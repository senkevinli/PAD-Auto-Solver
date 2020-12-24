#!/usr/bin/env python3

""" Class for simulating/easing board computations """
import heapq

from .pad_types import Orbs, Directions
from copy import deepcopy
from .board import Board
from typing import List, Tuple

def solve(raw_orbs, max_path):
    b = Board(raw_orbs)

    max = 0
    path = None
    start = None
<<<<<<< HEAD
    for y, orb_row in enumerate(raw_orbs):
        for x, orb in enumerate(orb_row):
            cur_max, cur_path = _solve_from((x, y), max_path, b)
            if cur_max > max:
                max = cur_max
                path = cur_path
                start = (x, y)
    # print(f'CURRENT MAX IS : {max}')
    return path, start
            
def _solve_from(start, max_path, b):
    visited = set()

    max_combos = b.max_combos()
    h = []

    # First element is the board, second is the list of directions
    # third is the starting point for the orb.
    # Use negative priority.

    initial_state = [b, [], start]
    initial_combos = b.calc_combos()
    heapq.heappush(
        h,
        (initial_combos, id(initial_state), initial_state)
    )

    visited.add(b.__str__())

    cur_combos = initial_combos

    max_combos_dir = []

    # BFS search.
    while len(h) > 0 and cur_combos < max_combos:

=======
    visited = set()
    for y, orb_row in enumerate(raw_orbs):
        for x, orb in enumerate(orb_row):
            cur_max, cur_path = _solve_from((x, y), max_path, b, visited)
            if cur_max > max:
                max = cur_max
                path = cur_path
                start = (x, y)
    # print(f'CURRENT MAX IS : {max}')
    return path, start
            
def _solve_from(start, max_path, b, visited):

    max_combos = b.max_combos()
    h = []

    # First element is the board, second is the list of directions
    # third is the starting point for the orb.
    # Use negative priority.

    initial_state = [b, [], start]
    initial_combos = b.calc_combos()
    heapq.heappush(
        h,
        (initial_combos, id(initial_state), initial_state)
    )

    visited.add(b.__str__())

    cur_combos = initial_combos

    max_combos_dir = []

    # BFS search.
    while len(h) > 0 and cur_combos < max_combos:

>>>>>>> debugging
        combos, _, (board, dir_list, start) = heapq.heappop(h)
        
        combos = abs(combos)

        if combos > cur_combos:
            cur_combos = combos
            max_combos_dir = dir_list

        if len(dir_list) >= max_path:
            continue

        for direction in Directions:
<<<<<<< HEAD
=======
            if len(dir_list) > 0 and direction == dir_list[-1]:
                continue
>>>>>>> debugging
            dup = Board(deepcopy(board.get_board()))
            valid = dup.move_orb(start, direction)
            if not valid:
                continue
            if dup.__str__() in visited:
                continue
            x, y = start
            next_loc = (x + direction.value[0], y + direction.value[1])

            next_combos = dup.calc_combos()

            combos = next_combos
            changed_dir_list = deepcopy(dir_list)
            changed_dir_list.append(direction)

            new_state = [dup, changed_dir_list, next_loc]
            heapq.heappush(
                h,
                (-combos, id(new_state), new_state)
            )

            visited.add(dup.__str__())
            
            cur_combos = max(combos, cur_combos)
            if cur_combos == combos:
                max_combos_dir = changed_dir_list
            
            if len(h) > 10:
                h = heapq.nsmallest(10, h)

    
    # print(len(h) == 0)
    # print(cur_combos >= max_combos)
    # print(f'FINAL: {cur_combos}')
<<<<<<< HEAD
=======
    logging.debug(f'Final for this iteration is: {cur_combos}')
>>>>>>> debugging

    return cur_combos, max_combos_dir