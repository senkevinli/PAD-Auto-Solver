import sys
import subprocess
import re
from ppadb.client import Client
from uiautomator import device as d

BOARD_ROWS = 5
BOARD_COLS = 6

# Assumes ratio is 16:9
WIDTH_RATIO = 9
HEIGHT_RATIO = 16

def configure_input(device):
    """Configures input so that swipes go to appropriate coordinates."""

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
    game_res_height = (res_width * HEIGHT_RATIO) // WIDTH_RATIO
    bar_height = (usable_res_height - game_res_height) // 2

    bottom_left_y = res_height - (navbar_height + bar_height)

    # Calculate radius of orbs.
    radius = (res_width // BOARD_COLS) // 2
    change = (res_width) // BOARD_COLS

    top_left_y = bottom_left_y - BOARD_ROWS * change 

    # Create 2d array of actual coordinates.
    coordinates = \
    [
        [
            (radius + col * change, top_left_y + radius + row * change)
            for col in range(BOARD_COLS)
        ] 
        for row in range(BOARD_ROWS)
    ]

    return coordinates

def path_string_to_coord(path_string, coordinates, start):
    x, y = start
    path_coord = []

    translator = {
        'L': (-1, 0),
        'U': (0, -1),
        'R': (1, 0),
        'D': (0, 1)
    }

    for op in path_string:
        coord = coordinates[y][x]
        path_coord.append(coord)

        direction = translator.get(op)
        
        # Error if not present.
        if direction is None:
            return None

        # Move x and y.
        x, y = tuple(
            map(lambda src, change: src + change, (x,y), direction)
        )

        if x < 0 or x >= BOARD_ROWS or y < 0 or y >= BOARD_COLS:
            return None

    path_coord.append(coordinates[y][x])
    return path_coord



if __name__ == '__main__':
    adb = Client(host='127.0.0.1', port=5037)
    devices = adb.devices()
    
    if len(devices) == 0:
        print('No devices attached.')
        sys.exit(0)

    device = devices[0]

    coordinates = configure_input(device)
    path_coord = path_string_to_coord ('RRRDDD', coordinates, (0,0))

    if path_coord is None:
        print('An error occurred.')
        sys.exit(0)

    print (path_coord)
    d.swipePoints(path_coord, steps=10)

