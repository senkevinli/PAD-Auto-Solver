import sys
import re
from ppadb.client import Client

BOARD_ROWS = 5
BOARD_COLS = 6

if __name__ == '__main__':
    adb = Client(host='127.0.0.1', port=5037)
    devices = adb.devices()
    
    if len(devices) == 0:
        print('No devices attached.')
        sys.exit(0)

    device = devices[0]

    # Configure movements based on resolution
    res_str = device.shell('wm size').replace('Physical size: ', '')
    res_width, res_height = list(map(int, res_str.split('x')))

    # Account for status bar/nav bar
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
    
    # Adjust res width/height to fit actually usable screen, assumes 16:9
    adj_res_height = res_height - statusbar_height - navbar_height
    


    # Orbs should move to the center
    dx = res_x // BOARD_COLS + (res_x // (BOARD_COLS * 2))

    
    # device.shell(f'input touchscreen swipe {dx} 1400 {dx} {1400 + dx}')
