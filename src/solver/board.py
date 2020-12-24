#!/usr/bin/env python3

""" Class for simulating/easing board computations """


from .pad_types import Orbs, Directions
from typing import List, Tuple
from copy import deepcopy

COMBO_LIMIT = 3
class Board:
    def __init__(self, orbs: List[List[Orbs]]) -> None:
        """
            Initializes a board. Stores orbs as a numpy array.
            List must be a list of Orb enums.
        """

        # Get the orbs frequency.        
        counts = {}


        for orb_row in orbs:
            for orb in orb_row:
                counts.update({orb: counts.get(orb, 0) + 1})

        # Constructive algorithm to calculate the max number of combos. Only
        # works for 6x5.
        # TODO: modify to account for 7x6 and 5x4 boards.
        max = 0
        exclude = None
        counts_copy = counts.copy()
        while True:
            pruned = {k: v for k, v in counts_copy.items() if v >= COMBO_LIMIT}
            key_list = list(pruned.keys())

            if exclude is not None and len(key_list) == 1 and key_list[0] == exclude:
                break

            # Get the next orb to be excluded and count the combo.
            exclude = next((orb for orb in key_list if orb != exclude), None)
            if exclude is None:
                break

            pruned.update({exclude: pruned.get(exclude) - COMBO_LIMIT})
            max += 1
            counts_copy = pruned

        # Set private variables.
        self.board = orbs
        self.rows = len(orbs)
        self.cols = len(orbs[0])
        self.counts = counts
        self.max = max

    def _erase_orbs(
        self,
        coord: Tuple[int, int],
        color: Orbs
    ) -> int:
        """
            Modifies board so that the combo starting at location
            specified by `start` is erased/set to `None`.

            TODO: Make more efficient, currently doing a lot of unnecessary recomputations.
            Also add in functionality for Ls and Crosses.
            
            NOTE:
            Assumes starting location is at the top left of the combo chain. Won't
            behave correctly otherwise.
        """
        self.a = 0

        def go_right(coord, color):
            """ Helper method for going right. """
            x, y = coord
            changed = 0

            right_b = x
            while right_b < self.cols:
                if self.board[y][right_b] != color and self.board[y][right_b] != Orbs.CLEARED:
                    break
                right_b += 1

            clearable = (right_b - x) >= COMBO_LIMIT
            for i in range(x, right_b):
                self.a += 1
                if clearable:
                    if self.board[y][i] != Orbs.CLEARED:
                        changed += 1
                    self.board[y][i] = Orbs.CLEARED
                elif i == x and self.board[y][i] != Orbs.CLEARED:
                    return changed
                if i != x:
                    changed += go_down((i,y), color)
            return changed
            

        def go_down(coord, color):
            """ Helper method for going down. """
            x, y = coord
            changed = 0

            down_b = y
            while down_b < self.rows:
                self.a += 1
                if self.board[down_b][x] != color and self.board[down_b][x] != Orbs.CLEARED:
                    break
                down_b += 1

            clearable = (down_b - y) >= COMBO_LIMIT
            for i in range(y, down_b):
                if clearable:
                    if self.board[i][x] != Orbs.CLEARED:
                        changed += 1
                    self.board[i][x] = Orbs.CLEARED
                elif i == y and self.board[i][x] != Orbs.CLEARED:
                    return changed
                if i != y:
                    changed += go_right((x, i), color)
            
            return changed
        sum = go_right(coord, color) + go_down(coord, color)
        return sum
                        

    def calc_combos(self) -> int:
        """
            Calculates the number of combos currently present on the board.
        """
        # Save current state because erase orbs will mutate the board.
        saved = deepcopy(self.board)

        def cleared_to_none():
            for y, orb_row in enumerate(self.board):
                for x, orb in enumerate(orb_row):
                    if (orb == Orbs.CLEARED):
                        self.board[y][x] = None

        combos = 0
        for y, orb_row in enumerate(self.board):
            for x, orb in enumerate(orb_row):
                if (orb != None):
                    if self._erase_orbs((x, y), orb) > 0:
                        combos = combos + 1
                        cleared_to_none()
        
        self.board = saved
        return combos
    
    def move_orb(self, src: Tuple[int, int], dir: Directions) -> bool:
        """
            Moves orb according to direction. Returns false if unable to.
        """
        x, y = src
        if x < 0 or y < 0 or x >= self.cols or y >= self.rows:
            return False

        x2 = x + dir.value[0]
        y2 = y + dir.value[1]

        if x2 < 0 or y2 < 0 or x2 >= self.cols or y2 >= self.rows:
            return False
        
        # Swap orbs.
        self.board[y][x], self.board[y2][x2] = self.board[y2][x2], self.board[y][x]
        return True
    
    def get_board(self):
        """
            Returns the board for hashing.
        """
        return self.board

    def max_combos(self):
        """
            Returns the maxmium # of combos.
        """
        return self.max

    def __str__(self):
        """
            String representation used for debugging.
        """
        string = ''
        for orb_rows in self.board:
            for orb in orb_rows:
                if orb is None:
                    orb = 'EMPTY'
                string += '{:<15}'.format(orb)
            string += '\n'
        return string

    def __lt__(self, other):
        return self.max_combos < other.max_combos
    
    def __hash__(self):
        """
            Hashing function based on the current board state.
        """
        converted = tuple(tuple(row) for row in self.board)
        return hash(self.board.__str__())
