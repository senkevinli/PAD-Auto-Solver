#!/usr/bin/env python3

import re
from ppadb.client import Client
from uiautomator import Device

class Interface:
    def __init__(
        self,
        board_rows: int = 5,
        board_cols: int = 6,
        width_ratio: int = 9,
        height_ratio: int = 16,
        swipe_ms: int = 25
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
        self.ms = swipe_ms

        # Device specific info.
        self.device = None
        self.coordinates = None

        self.top_left = None
        self.top_right = None
        self.bottom_left = None
        self.bottom_right = None


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
        bar_height = (usable_res_height - game_res_height) // 2

        bottom_y = res_height - (navbar_height + bar_height)

        # Calculate radius of orbs.
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
        self.device = Device(device.shell('adb shell getprop ro.serialno'))

        # For PAD board dimensions/coordinates
        self.bottom_left = (0, bottom_y)
        self.bottom_right = (res_width, bottom_y)
        self.top_left = (0, top_y)
        self.top_right = (res_width, top_y)

        return True

