#!/usr/bin/env python3

import sys
from solver.interface import Interface
from solver.pad_types import Directions
from solver.detector import detect

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

    raw_orbs = interface.board_screencap()
    detected = detect(raw_orbs)

    if (detected is None):
        print('Error in detection.')
