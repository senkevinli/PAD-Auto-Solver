#!/usr/bin/env python3

""" For the actual solving of the board. Prioritizes combos. """
import heapq
import logging

from .pad_types import Orbs, Directions
from copy import deepcopy
from .board import Board
from typing import List, Tuple

HEAP_SIZE = 10

class SolveState:
    def __init__(
        self,
        board: List[List[Orbs]],
        dir_list: List[Directions],
        cur: Tuple[int, int]
    ) -> None:
        self.board = board
        self.dir_list = dir_list
        self.cur = cur
        combos, clusters = self.board.calc_combos()
        self.combos = combos

        self.board.sub_cluster(clusters)
        self.potential = self.board.get_potential() 

    def __lt__(self, other):
        """
            Reverse less than function for the heap.
            Edit this function here if you want to sort 
            by a different criteria.
        """
        if self.combos == other.combos:
            return self.potential > other.potential
        return self.combos > other.combos

def solve(
        raw_orbs: List[List[Orbs]],
        max_path: int
    ) -> Tuple[List[Directions], Tuple[int, int], int]:
    """
        Solves according to the `raw_orbs` list provided and the
        `max_path` specified. Returns a tuple of the list of directions
        to underatke, a starting coordinate, and the number of combos made,
        respectively.
    """
    b = Board(raw_orbs)

    logging.debug('Try to solve:')
    logging.debug(b)

    max_combos = 0
    best = None
    start = (0, 0)

    for y, orb_row in enumerate(raw_orbs):
        for x, _ in enumerate(orb_row):
            ideal = _solve_from((x, y), max_path, b)
            if ideal.combos > max_combos:
                max_combos = ideal.combos
                best = ideal
                start = (x, y)
    
    logging.debug(f'Optimal combos is : {max_combos}')
    logging.debug('Path is:')
    logging.debug(best.dir_list)
    return best.dir_list, start, best.combos

def _solve_from(
        start: Tuple[int, int],
        max_path: int,
        b: Board
    ) -> SolveState:
    """
        Takes a step solve from the specified coordinate
        of `start`. Uses a modified greedy BFS approach
        with a fixed size priority queue (min heap).
    """
    initial_state = SolveState(b, [], start)
    max_combos = b.get_potential()

    # Our heap/priority queue for greedy BFS.
    h = []

    heapq.heappush(h, initial_state)

    cur_combos = initial_state.combos
    ideal = initial_state

    # BFS search.
    while len(h) > 0 and cur_combos < max_combos:
        prev_state = heapq.heappop(h)
        combos = prev_state.combos

        if combos > cur_combos:
            ideal = prev_state
            cur_combos = combos

        if len(prev_state.dir_list) >= max_path:
            continue

        for direction in Directions:

            # Skip redundant move so we don't end up going back.
            if len(prev_state.dir_list) > 0:
                last_move = prev_state.dir_list[-1]
                if direction == Directions.DOWN and last_move == Directions.UP:
                    continue
                elif direction == Directions.UP and last_move == Directions.DOWN:
                    continue
                elif direction == Directions.LEFT and last_move == Directions.RIGHT:
                    continue
                elif direction == Directions.RIGHT and last_move == Directions.LEFT:
                    continue

            x, y = prev_state.cur
            next_loc = (x + direction.value[0], y + direction.value[1])

            if not prev_state.board.in_bounds(next_loc):
                continue

            next_board = Board(prev_state.board.get_board())
            valid = next_board.move_orb(prev_state.cur, direction)

            if not valid:
                continue

            changed_dir_list = deepcopy(prev_state.dir_list)
            changed_dir_list.append(direction)

            next_state = SolveState(next_board, changed_dir_list, next_loc)

            if next_state.combos > cur_combos:
                ideal = next_state
                combos = next_state.combos

            heapq.heappush(h, next_state)

        if len(h) > HEAP_SIZE:
            h = heapq.nsmallest(HEAP_SIZE, h)


    logging.debug(f'Final for this iteration is: {cur_combos}')

    return ideal
