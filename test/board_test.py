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
    ret = b._erase_orbs((1, 0), Orbs.BLUE)

    assert ret == 11
    assert getattr(b, 'board') == output_1

def test_erase_2():
    """ Check if it doesn't erase unnecessary orbs. """
    data = parse_json_file('board1')
    
    input_1 = data.get('board_input')
    output_1 = deepcopy(input_1)

    b = Board(input_1)
    ret = b._erase_orbs((0, 3), Orbs.LIGHT)

    assert ret == 0
    assert getattr(b, 'board') == output_1

def test_erase_3():
    """ Check if it erases all orbs except 1."""
    data = parse_json_file('board2')
    
    input_2 = data.get('board_input')
    output_2 = data.get('board_erase_output')

    b = Board(input_2)
    ret = b._erase_orbs((0, 0), Orbs.LIGHT)
    assert ret == 29
    # Everything should be erased except for last orb.
    assert getattr(b, 'board') == output_2

def test_erase_4():
    """ Trying another pattern."""
    data = parse_json_file('board3')
    
    input_3 = data.get('board_input')
    output_3 = data.get('board_erase_output')
    b = Board(deepcopy(input_3))
    ret = b._erase_orbs((0, 3), Orbs.LIGHT)
    assert ret == 11
    assert getattr(b, 'board') == output_3

def test_erase_5():
    """ L Formation."""
    data = parse_json_file('board4')
    
    input_4 = data.get('board_input')
    output_4 = data.get('board_erase_output')
    b = Board(deepcopy(input_4))
    ret = b._erase_orbs((1, 0), Orbs.BLUE)

    assert ret == 7
    assert getattr(b, 'board') == output_4

def test_erase_6():
    """ Square Formation."""
    data = parse_json_file('board5')
    
    input_5 = data.get('board_input')
    output_5 = data.get('board_erase_output')
    b = Board(deepcopy(input_5))
    ret = b._erase_orbs((1, 0), Orbs.BLUE)

    assert ret == 0
    assert getattr(b, 'board') == output_5

def test_erase_7():
    """ Offset T Formation."""
    data = parse_json_file('board6')
    
    input_6 = data.get('board_input')
    output_6 = data.get('board_erase_output')
    b = Board(deepcopy(input_6))
    ret = b._erase_orbs((1, 0), Orbs.BLUE)

    assert ret == 5
    assert getattr(b, 'board') == output_6

def test_erase_8():
    """ Zigzag Formation."""
    data = parse_json_file('board7')
    
    input_7 = data.get('board_input')
    output_7 = data.get('board_erase_output')
    b = Board(deepcopy(input_7))
    ret = b._erase_orbs((0, 0), Orbs.LIGHT)

    assert ret == 13
    assert getattr(b, 'board') == output_7

def test_erase_8():
    """ Uneven Square Formation."""
    data = parse_json_file('board8')
    
    input_8 = data.get('board_input')
    output_8 = data.get('board_erase_output')
    b = Board(deepcopy(input_8))
    ret = b._erase_orbs((0, 0), Orbs.LIGHT)

    assert ret == 7
    assert getattr(b, 'board') == output_8

def test_erase_all_1():
    """ Uneven Square Formation."""
    data = parse_json_file('board3')
    
    inp = data.get('board_input')
    outp = data.get('board_erase_all_output')
    b = Board(deepcopy(inp))
    ret = b.calc_combos()

    assert ret == 3
    assert getattr(b, 'board') == outp