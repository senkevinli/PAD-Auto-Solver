#!/usr/bin/env python3

""" For translating Dawnglare strings. Used for testing. """

BOARD_ROWS = 5
BOARD_COLS = 6

def str_to_enum() -> None:
    
    string = input('Enter Dawnglare String: ')
    mapping = {
        'L': 'Orbs.LIGHT',
        'B': 'Orbs.BLUE',
        'G': 'Orbs.GREEN',
        'R': 'Orbs.RED',
        'D': 'Orbs.DARK',
        'H': 'Orbs.HEART'
    }

    row = []
    for char in string:
        row.append(mapping.get(char))
        if len(row) == BOARD_COLS:
            to_print = '[ '
            for orb in row:
                to_print += f'{orb}, '
            to_print += ']'
            
            print(to_print)
            row = []

if __name__ == '__main__':
    str_to_enum()