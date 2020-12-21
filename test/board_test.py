#!/usr/bin/env python3

import os
import json

from copy import deepcopy
from src.solver.board import Board
from src.solver.pad_types import Orbs
from PIL import Image
from typing import List

def parse_json_file(name: str) -> List[List[Orbs]]:
    """ 
    Gets JSON file and converts it to a list of list of enums. Utility
    function for testing.
    """
    dirname = os.path.dirname(__file__)
    name = os.path.join(dirname, f'fixtures/boards/{name}.json')

    with open(name) as f:
        data = json.load(f)
        for key in data.keys():
            mod_list = [[Orbs[name] for name in row] for row in data.get(key)]
            data.update({key: mod_list})

    return data

def test_erase_1():
    """ Check if able to erase consecutive orbs. """
    
    data = parse_json_file('board1')
    
    input_1 = data.get('board_input')
    output_1 = data.get('board_erase_output')

    b = Board(input_1)
    b._erase_orbs((1, 0), Orbs.BLUE, (0, 0))
    assert getattr(b, 'board') == output_1

def test_erase_2():
    """ Check if it doesn't erase unnecessary orbs. """
    data = parse_json_file('board1')
    
    input_1 = data.get('board_input')
    output_1 = deepcopy(input_1)

    b = Board(input_1)
    b._erase_orbs((0, 3), Orbs.LIGHT, (0, 0))

    # Should still be the same.
    assert getattr(b, 'board') == output_1

def test_erase_3():
    """ Check if it erases all orbs except 1."""
    data = parse_json_file('board2')
    
    input_2 = data.get('board_input')
    output_2 = data.get('board_erase_output')

    b = Board(input_2)
    b._erase_orbs((0, 0), Orbs.LIGHT, (0,0))

    # Everything should be erased except for last orb.
    assert getattr(b, 'board') == output_2

def test_erase_4():
    """ Trying another pattern."""
    data = parse_json_file('board3')
    
    input_3 = data.get('board_input')
    output_3 = data.get('board_erase_output')
    b = Board(deepcopy(input_3))
    b._erase_orbs((0, 3), Orbs.LIGHT, (0, 0))

    # Everything should be erased except for last orb.
    assert getattr(b, 'board') == output_3