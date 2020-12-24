#!/usr/bin/env python3

import logging
import sys
import click
import time
from pyfiglet import print_figlet
from yaspin import yaspin
from PyInquirer import prompt
from typing import List, Dict

try:
    from .solver.interface import Interface
    from .solver.pad_types import Directions
    from .solver.detector import detect
    from .solver.board import Board
    from .solver.solver import solve
except:
    from solver.interface import Interface
    from solver.pad_types import Directions
    from solver.detector import detect
    from solver.board import Board
    from solver.solver import solve

BOARD_ROWS = 5
BOARD_COLS = 6

# Only 16:9 ratio supported.
WIDTH_RATIO = 9
HEIGHT_RATIO = 16

SPEED = 30

def _gen_confirm(msg: str) -> List[Dict]:
    """ For generating a confirmation prompt. """
    return [
        {
            'type': 'confirm',
            'message': msg,
            'name': 'confirmation'
        }
    ]

def _handle_error():
    """ For any errors. """
    answer = prompt(_gen_confirm('Continue?'))
    if not answer.get('confirmation'):
        sys.exit(0)

@click.command()
@click.option('--rows', default=BOARD_ROWS, help='Number of rows.')
@click.option('--cols', default=BOARD_COLS, help='Number of rows. ')
@click.option('--speed', default=SPEED, help='Time(ms) for orb swipe.')
@click.option('-v', '--verbose', default=False, help='Verbose output for debugging.')
def main(rows, cols, speed, verbose):
    """ Main loop for evaluating. """

    # Configure logger.
    log_level = logging.INFO if not verbose else logging.DEBUG
    # Configure logger.
    # logging.basicConfig(
    #     stream=sys.stdout,
    #     level=log_level,
    #     format='%(message)s'
    # )
    # For prompting.

    print_figlet('Puzzles and Dragons Solver', font='slant', colors='CYAN')

    # Configure device.
    interface = None
    while True:
        with yaspin(text='Setting up device', color='cyan') as sp:
            interface = Interface(rows, cols, WIDTH_RATIO, HEIGHT_RATIO, speed)
            if (not interface.setup_device()):
                sp.fail('Error in setting up device. Please check if device is attacked.')
            else:
                sp.ok('Setup successful')
                break

        _handle_error()
    
    answer = prompt(_gen_confirm('Proceed with solving?'))
    if not answer.get('confirmation'):
        sys.exit(0)

    # Start solving.
    while True:
        with yaspin(text='Solving', color='cyan') as sp:
            raw_orbs = interface.board_screencap()
            if raw_orbs is None:
                sp.fail('Error in taking a screenshot.')
                _handle_error()
                continue

            sp.write('> screenshot taken.')
            detected = detect(raw_orbs)

            if detected is None:
                sp.fail('Error in detection.')
                _handle_error()
                continue

            sp.write('> finished detection.')
            path, start = solve(detected, 75)
            sp.write('> path found.')
            interface.input_swipes(path, start)
            sp.ok()
        answer = prompt(_gen_confirm('Proceed with solving?'))
        if not answer.get('confirmation'):
            sys.exit(0)



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
