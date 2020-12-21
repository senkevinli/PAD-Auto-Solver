#!/usr/bin/env python3

import os
from copy import deepcopy
from src.solver.board import Board
from src.solver.pad_types import Orbs
from PIL import Image

board1_input = \
[
    [ Orbs.LIGHT, Orbs.BLUE, Orbs.BLUE, Orbs.BLUE, Orbs.BLUE, Orbs.BLUE ],
    [ Orbs.RED, Orbs.BLUE, Orbs.BLUE, Orbs.BLUE, Orbs.GREEN, Orbs.HEART ],
    [ Orbs.RED, Orbs.BLUE, Orbs.BLUE, Orbs.BLUE, Orbs.HEART, Orbs.GREEN ],
    [ Orbs.LIGHT, Orbs.HEART, Orbs.LIGHT, Orbs.LIGHT, Orbs.DARK, Orbs.RED ],
    [ Orbs.LIGHT, Orbs.LIGHT, Orbs.GREEN, Orbs.RED, Orbs.RED, Orbs.BLUE]
]

board1_output = \
[
    [ Orbs.LIGHT, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED ],
    [ Orbs.RED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.GREEN, Orbs.HEART ],
    [ Orbs.RED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.HEART, Orbs.GREEN ],
    [ Orbs.LIGHT, Orbs.HEART, Orbs.LIGHT, Orbs.LIGHT, Orbs.DARK, Orbs.RED ],
    [ Orbs.LIGHT, Orbs.LIGHT, Orbs.GREEN, Orbs.RED, Orbs.RED, Orbs.BLUE]
]

board2_input = \
[
    [ Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT ],
    [ Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT ],
    [ Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT ],
    [ Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT ],
    [ Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.BLUE]
]

board2_output = \
[
    [ Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED ],
    [ Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED ],
    [ Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED ],
    [ Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED ],
    [ Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.BLUE]
]

board3_input = \
[
    [ Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT ],
    [ Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT ],
    [ Orbs.DARK, Orbs.DARK, Orbs.DARK, Orbs.DARK, Orbs.DARK, Orbs.DARK ],
    [ Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT ],
    [ Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.BLUE]
]

board3_output = \
[
    [ Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT ],
    [ Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT, Orbs.LIGHT ],
    [ Orbs.DARK, Orbs.DARK, Orbs.DARK, Orbs.DARK, Orbs.DARK, Orbs.DARK ],
    [ Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED ],
    [ Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.CLEARED, Orbs.BLUE]
]

def test_erase_1():
    """ Check if able to erase consecutive orbs. """
    b = Board(deepcopy(board1_input))
    b._erase_orbs((1, 0), Orbs.BLUE, (0, 0))
    assert getattr(b, 'board') == board1_output

def test_erase_2():
    """ Check if it doesn't erase unnecessary orbs. """
    b = Board(deepcopy(board1_input))
    b._erase_orbs((0, 3), Orbs.BLUE, (0, 0))

    # Should still be the same.
    assert getattr(b, 'board') == board1_input

def test_erase_3():
    """ Check if it erases all orbs except 1."""
    b = Board(deepcopy(board2_input))
    b._erase_orbs((0, 0), Orbs.LIGHT, (0, 0))

    # Everything should be erased except for last orb.
    assert getattr(b, 'board') == board2_output

def test_erase_4():
    """ Trying another pattern."""
    b = Board(deepcopy(board3_input))
    b._erase_orbs((0, 3), Orbs.LIGHT, (0, 0))

    # Everything should be erased except for last orb.
    assert getattr(b, 'board') == board3_output
