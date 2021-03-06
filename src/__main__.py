
#!/usr/bin/env python3

import logging
import sys
import click
from datetime import datetime
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

# Constants.
BOARD_ROWS = 5
BOARD_COLS = 6

WIDTH_RATIO = 9
HEIGHT_RATIO = 16

MAX_PATH = 25
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

def _debug(rows, cols, speed, path):
    """ For verbose output/debug. No spinners. """
    interface = Interface(rows, cols, WIDTH_RATIO, HEIGHT_RATIO, speed)

    if (not interface.setup_device()):
        print('Error in setting up device. Please check if device is attached.')
        sys.exit(0)
    print('> device setup.')

    raw_orbs = interface.board_screencap()

    print('> screenshot taken.')
    detected = detect(raw_orbs)

    if (detected is None):
        print('Error in detection.')
        sys.exit(0)
    print('> detection complete')

    path, start, _ = solve(detected, path)
    print('solved.')
    interface.input_swipes(path, start)

def _non_verbose(rows, cols, speed, max_path):
    """ For non-verbose output. With spinners. """
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

            begin = datetime.now()
            path, start, combos = solve(detected, max_path)
            end = datetime.now()

            delta = end - begin
            sp.write(f'> {combos} combo(s) path found in {delta.total_seconds()} seconds!')
            interface.input_swipes(path, start)
            sp.ok()
        answer = prompt(_gen_confirm('Proceed with solving?'))
        if not answer.get('confirmation'):
            sys.exit(0)

@click.command()
@click.option('--rows', default=BOARD_ROWS, help='Number of rows.')
@click.option('--cols', default=BOARD_COLS, help='Number of rows. ')
@click.option('--speed', default=SPEED, help='Time(ms) for orb swipe.')
@click.option('-d', '--debug', default=False, help='Verbose output for debugging.')
@click.option('-p', '--path', default=MAX_PATH, help='The maxmium length of the path.')
def main(rows, cols, speed, debug, path):
    """ Main loop for evaluating. """
    print_figlet('Puzzles and Dragons Solver', font='slant', colors='CYAN')
    
    # Prevent PIL pollution.
    pil_logger = logging.getLogger('PIL')
    pil_logger.setLevel(logging.INFO)

    logging.basicConfig(
        stream=sys.stdout,
        level=logging.CRITICAL if not debug else logging.DEBUG,
        format='%(message)s'
    )

    if not debug:
        _non_verbose(rows, cols, speed, path)
    else:
        _debug(rows, cols, speed, path)



if __name__ == '__main__':
    main()