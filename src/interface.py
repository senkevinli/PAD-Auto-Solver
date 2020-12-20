#!/usr/bin/env python3

import re
from PIL import Image
from os import path, remove
from ppadb.client import Client
from uiautomator import AutomatorDevice
from copy import deepcopy
from typing import List, Tuple
from pad_types import Directions

dirname = path.dirname(__file__)
LOCATION = path.join(dirname, 'screen.png')

class Interface:
    def __init__(
        self,
        board_rows: int = 5,
        board_cols: int = 6,
        width_ratio: int = 9,
        height_ratio: int = 16,
        swipe_ms: int = 50
    ) -> None:
        """
        Args:
            `board_rows`: number of rows for PAD board.
            `board_cols`: number of columns for PAD board.
            `width_ratio`: in-game aspect ratio for width.
            `height_ratio`: in-game aspect ratio for height.
            `swipe_ms`: time in ms to move one orb to another location.
        """

        # Info for configuration.
        self.board_rows = board_rows
        self.board_cols = board_cols
        self.width_ratio = width_ratio
        self.height_ratio = height_ratio
        self.ms = swipe_ms

        # Device specific info.
        self.device = None
        self.coordinates = None

        self.top = None
        self.right = None
        self.left = None
        self.bottom = None


    def setup_device(self) -> bool:
        """
        Sets up device through Android Debug Bridge in local port 5037.
        Returns whether or not successful. Currently only supports 16x9
        aspect ratios.
        """
        adb = Client(host='127.0.0.1', port=5037)
        devices = adb.devices()
    
        if len(devices) == 0:
            return False

        device = devices[0]

            # Configure movements based on resolution.
        res_str = device.shell('wm size').replace('Physical size: ', '')
        res_width, res_height = list(map(int, res_str.split('x')))

        # Account for status bar/nav bar.
        navbar_str = device.shell(
            "dumpsys window windows | sed -n '/Window .*NavigationBar.*" \
            ":/,/Window .*:/p' | grep 'Requested'"
            )

        statusbar_str = device.shell(
            "dumpsys window windows | sed -n '/Window .*StatusBar.*" \
            ":/,/Window .*:/p' | grep 'Requested'"
            )

        nav_match = re.search('h=(\d+)', navbar_str)
        navbar_height = int(nav_match.group(1)) if nav_match else 0

        status_match = re.search('h=(\d+)', statusbar_str)
        statusbar_height = int(status_match.group(1)) if status_match else 0

        # Adjust res width/height to fit actually usable screen.
        usable_res_height = res_height - statusbar_height - navbar_height

        # PAD uses black bars to pad screen in order to fit aspect ratio.
        # Calculate the height of the bars so that we can locate lower left corner.
        game_res_height = (res_width * self.height_ratio) // self.width_ratio
        bar_height = (usable_res_height - game_res_height)

        bottom_y = res_height - (navbar_height + bar_height)

        # Calculate radius of orbs and how much to shift when moving.
        radius = (res_width // self.board_cols) // 2
        change = (res_width) // self.board_cols

        top_y = bottom_y - self.board_rows * change 

        # Create 2d array of actual coordinates.
        coordinates = \
        [
            [
                (radius + col * change, top_y + radius + row * change)
                for col in range(self.board_cols)
            ] 
            for row in range(self.board_rows)
        ]

        # Set private variables.
        self.coordinates = coordinates
        self.device = AutomatorDevice()

        # For PAD board dimensions/coordinates
        self.bottom = bottom_y
        self.top = top_y
        self.left = 0
        self.right = res_width

        return True

    def _path_to_coord(
            self,
            path: List[Directions],
            start: Tuple[int, int]
        ) -> List[Tuple[int, int]]:
        """
            Takes in a list of directions and converts it to 
            actual pixel coordinates on the phone. Returns None
            if errored.
        """

        x, y = start
        if x < 0 or x >= self.board_cols or y < 0 or y >= self.board_rows:
            return None
        
        if len(path) <= 1:
            return None

        path_coord = []

        for op in path:
            coord = self.coordinates[y][x]
            path_coord.append(deepcopy(coord))

            direction = op.value
            
            # Error if not present.
            if direction is None:
                return None

            # Move x and y.
            x, y = tuple(
                map(lambda src, change: src + change, (x,y), direction)
            )

            if x < 0 or x >= self.board_cols or y < 0 or y >= self.board_rows:
                return None

        # Get the last coordinate.
        path_coord.append(deepcopy(self.coordinates[y][x]))
        return path_coord

    def input_swipes(
            self,
            path: List[Directions],
            start: Tuple[int, int]
        ) -> None:
        """
            Takes in a list of directions and inputs
            the swipes to the phone. Requires that `setup_device`
            has been called.
        """
        path_coord = self._path_to_coord(path, start)

        # If errored out, return None.
        if not path_coord:
            return None

        mod_steps = self.ms // 5
        self.device.swipePoints(path_coord, mod_steps)
    
    def board_screencap(self) -> List[Image.Image]:
        """
            Captures the screen and returns the cropped
            board as a PIL.Image.
        """
        self.device.screenshot(LOCATION)
        with Image.open(LOCATION) as im:
            orbs = []

            # Get specfic orbs.
            # Layout is like:
            # 0 ... len(orbs[0])
            # .
            # .
            # .
            # len(orbs)

            dx = (self.right - self.left) // self.board_cols
            dy = (self.bottom - self.top) // self.board_rows

            for row in range(self.board_rows):
                for col in range(self.board_cols):
                    orb = im.crop((
                        self.left + dx * col,
                        self.top + dy * row,
                        self.left + dx * (col + 1),
                        self.top + dy * (row + 1)
                    ))
                    orbs.append(orb)

            # Remove screencap after getting orbs.
            remove(LOCATION)
        return orbs



