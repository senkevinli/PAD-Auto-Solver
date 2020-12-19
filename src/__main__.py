#!/usr/bin/env python3

import sys
from interface import Interface
from pad_types import Directions

BOARD_ROWS = 5
BOARD_COLS = 6

# Assumes ratio is 16:9
WIDTH_RATIO = 9
HEIGHT_RATIO = 16

if __name__ == '__main__':

    interface = Interface(BOARD_ROWS, BOARD_COLS, WIDTH_RATIO, HEIGHT_RATIO)

    if (not interface.setup_device()):
        print('Error in setting up device. Please check if device is attached.')
        sys.exit(0)

    dir = [Directions.LEFT, Directions.LEFT, Directions.UP, Directions.UP, Directions.RIGHT,
           Directions.DOWN]

    interface.input_swipes(dir, (4,2))

