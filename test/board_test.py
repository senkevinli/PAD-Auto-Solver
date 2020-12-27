#!/usr/bin/env python3

import os
import json
from pprint import pprint

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

    b = Board(input_1)
    combos, clusters = b.calc_combos()
    assert combos == 1

    # First `Blue` combo set should be length 11.
    assert len(clusters.get(Orbs.BLUE)[0]) == 11
    b.sub_cluster(clusters)
    assert b.get_potential() == 5

def test_erase_2():
    """ Check if it erases all orbs except 1."""
    data = parse_json_file('board2')
    
    input_2 = data.get('board_input')

    b = Board(input_2)
    combos, clusters = b.calc_combos()
    
    assert combos == 1
    assert len(clusters.get(Orbs.LIGHT)) == 1
    assert len(clusters.get(Orbs.LIGHT)[0]) == 29

def test_erase_3():
    """ Trying another pattern."""
    data = parse_json_file('board3')
    
    input_3 = data.get('board_input')

    b = Board(input_3)
    combos, clusters = b.calc_combos()
    
    assert combos == 3

    # Should be two clusters.
    assert len(clusters.get(Orbs.LIGHT)) == 2
    assert len(clusters.get(Orbs.LIGHT)[0]) == 12
    assert len(clusters.get(Orbs.LIGHT)[1]) == 11
    assert len(clusters.get(Orbs.DARK)[0]) == 6


def test_erase_4():
    """ L Formation."""
    data = parse_json_file('board4')
    
    input_4 = data.get('board_input')
    b = Board(input_4)
    combos, clusters = b.calc_combos()

    assert combos == 1
    assert len(clusters.get(Orbs.BLUE)[0]) == 7

def test_erase_5():
    """ Square Formation. Should not clear."""
    data = parse_json_file('board5')
    
    input_5 = data.get('board_input')
    b = Board(input_5)
    combos, clusters = b.calc_combos()

    assert combos == 0
    
    for cluster in clusters.values():
        assert len(cluster) == 0

def test_erase_6():
    """ Offset cross formation with cascade. """
    data = parse_json_file('board6')
    
    input_6 = data.get('board_input')
    b = Board(input_6)
    combos, clusters = b.calc_combos()

    assert combos == 3
    # 2 clusters, 1 from cascade.
    assert len(clusters.get(Orbs.LIGHT)) == 2
    
    # Check if cross is OK.
    assert len(clusters.get(Orbs.BLUE)[0]) == 5
def test_erase_7():
    """ Zigzag Formation with 2 step cascade. """
    data = parse_json_file('board7')
    
    input_7 = data.get('board_input')
    b = Board(input_7)
    combos, clusters = b.calc_combos()

    assert combos == 3
    assert len(clusters.get(Orbs.LIGHT)[0]) == 13
    assert len(clusters.get(Orbs.GREEN)[0]) == 3
    assert len(clusters.get(Orbs.BLUE)[0]) == 3

def test_erase_8():
    """ Same color cascade."""
    data = parse_json_file('board8')
    
    input_8 = data.get('board_input')
    b = Board(input_8)
    combos, clusters = b.calc_combos()

    assert combos == 3
    assert len(clusters.get(Orbs.LIGHT)) == 2
    assert len(clusters.get(Orbs.HEART)[0]) == 3

def test_erase_9():
    """ More complex cascade. """
    data = parse_json_file('board9')
    
    inp = data.get('board_input')
    b = Board(inp)
    combos, clusters = b.calc_combos()

    assert combos == 5

def test_erase_10():
    """ Another complex cascade. """
    data = parse_json_file('board10')
    
    inp = data.get('board_input')
    b = Board(inp)
    combos, clusters = b.calc_combos()
    pprint(clusters)
    print(combos)