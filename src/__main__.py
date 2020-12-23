#!/usr/bin/env python3

import logging
import sys
import click
from pyfiglet import Figlet

from .solver.interface import Interface
from .solver.pad_types import Directions
from .solver.detector import detect
from .solver.board import Board
from .solver.solver import solve

BOARD_ROWS = 5
BOARD_COLS = 6

# Assumes ratio is 16:9
WIDTH_RATIO = 9
HEIGHT_RATIO = 16

@click.command()
@click.option('--row', default=BOARD_ROWS, help='Number of rows.')
@click.option('--cols', default=BOARD_COLS, help='Number of rows. ')
def main(row, cols):
    print(row)
    print(cols)

if __name__ == '__main__':
    main()
    # # Configure logger.
    # logging.basicConfig(
    #     stream=sys.stdout,
    #     level=logging.CRITICAL,
    #     format='%(message)s'
    # )

    # logging.info('hia')
    
    # f = Figlet(font='slant')
    # print(f.renderText('Puzzles and Dragons Solver'))
    # interface = Interface(BOARD_ROWS, BOARD_COLS, WIDTH_RATIO, HEIGHT_RATIO, 30)

    # logging.debug('hi')
    # # if (not interface.setup_device()):
    # #     print('Error in setting up device. Please check if device is attached.')
    # #     sys.exit(0)

    # # raw_orbs = interface.board_screencap()
    # # detected = detect(raw_orbs)

    # # if (detected is None):
    # #     print('Error in detection.')
    # #     sys.exit(0)

    # # path, start = solve(detected, 50)
    # # print('solved.')
    # # print(path, start)
    # # errored = interface.input_swipes(path, start)
