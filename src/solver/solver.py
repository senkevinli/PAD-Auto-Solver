#!/usr/bin/env python3

""" Class for simulating/easing board computations """
import heapq
import logging

from .pad_types import Orbs, Directions
from copy import deepcopy
from .board import Board
from typing import List, Tuple, Set

class SolveState:
    """ Class to keep track of the solution state. """

    def __init__(
        self,
        b: Board,
        dir_list: List[Directions],
        start: Tuple[int, int],
        current: Tuple[int, int]
    ) -> None:
        """
            Creates a new SolveState from the current state of
            the board, the current direction list, and the starting
            coordinate. Makes a deepcopy of the board.
        """
        self.board = Board(deepcopy(b.get_board()))
        self.dir_list = [] if len(dir_list) == 0 else deepcopy(dir_list)
        self.start = start
        self.current = current
        self.combos = self.board.calc_combos()

    def combos(self) -> int:
        """
            Returns the # of combos currently present on the board.
        """
        return self.combos
    

    def dir_list(self) -> List[Directions]:
        """
            Returns the direction path.
        """
        return self.dir_list

    def get_start(self) -> Tuple[int, int]:
        """
            Returns the starting coordinate.
        """
        return self.start
    
    def move_current(self, dir: Directions) -> bool:
        """
            Moves an orb on the board based on the direction
            and the current orb in the state.
        """
        new_cur = self.board.move_orb(self.current, dir)
        if new_cur is not None:
            self.current = new_cur

            # Recalculate combos
            self.combos = self.board.calc_combos()
            return True
        return False

    def __hash__(self):
        """ 
            Hash function will be use the board.
        """
        return hash(self.board)
    def __eq__(self, other):
        return True

    def __lt__(self, other):
        """ 
            Comparison function for sorting. Inverted
            for the min heap.
        """
        if not isinstance(other, SolveState):
            return NotImplemented
        return self.combos > other.combos
        

def solve(
    orbs: List[List[Orbs]],
    max_path: int
) -> Tuple[List[Directions], Tuple[int, int]]:
    """
        Solves the board by iterating through all the 
        starting coordinates and starting a BFS search.

        Returns the directions list and the starting coordinates
        of the calculated optimal path.
    """
    b = Board(orbs)
    visited = set()

    sol_list = \
    [
        _solve_from((x, y), max_path, b, visited) 
        for y, orb_row in enumerate(orbs)
        for x, _ in enumerate(orb_row)
    ]

    sol_list.sort()

    best = sol_list[0]
    max_combos = best.combos
    path = best.dir_list
    start = best.start

    logging.debug(f'Solve max is: {max_combos}')
    return path, start
            
def _solve_from(
    start: Tuple[int, int],
    max_path: int,
    b: Board,
    visited: Set
) -> SolveState:
    """
        Modified BFS search with a priority queue
        from the starting location. Returns the
        calculated optimal solution state from 
        the starting point. 
    """

    # Fixed size priority queue using a heap.
    h = []

    initial = SolveState(b, [], start, start)

    heapq.heappush(h, initial)
    visited = set()
    visited.add(initial)

    if initial in visited:
        print('???')

    cur_combos = initial.combos

    opt_sol = None

    # Modified BFS search.
    while len(h) > 0 and cur_combos < 10:

        state = heapq.heappop(h)
        combos = state.combos
        dir_list = state.dir_list

        # If the popped state has the greatest amount of combos
        # so far.
        if combos >= cur_combos:
            cur_combos = combos
            opt_sol = state

        # If the max path is too long, don't iterate through directions.
        if len(dir_list) >= max_path:
            continue

        for direction in Directions:

            if len(dir_list) > 0 and direction == dir_list[-1]:
                continue
            next_state = SolveState(
                state.board,
                state.dir_list,
                state.start,
                state.current
            )

            
            valid = next_state.move_current(direction)

            if not valid:
                continue
            if next_state in visited:
                continue
                
            # Unique and succesful state. Add the direction.
            next_state.dir_list.append(direction)
            heapq.heappush(h, next_state)

            visited.add(next_state)
            
            if len(h) > 10:
                h = heapq.nsmallest(10, h)

    
    # print(len(h) == 0)
    # print(cur_combos >= max_combos)
    # print(f'FINAL: {cur_combos}')
    logging.debug(f'Finished this iteration: {opt_sol.combos}')

    return opt_sol