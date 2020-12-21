#!/usr/bin/env python3

""" Class for simulating/easing board computations """


from .pad_types import Orbs, Directions
from typing import List, Tuple

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
        color: Orbs,
        chain: Tuple[int, int]
    ) -> Tuple[int, int]:
        """
            Modifies board so that the combo starting at location
            specified by `start` is erased/set to `None`. 
            
            NOTE:
            Assumes starting location is at the top left of the combo chain. Won't
            behave correctly otherwise.
        """
        x, y = coord
        
        # Return silently if out of bounds.
        if x >= self.cols or x < 0 or y >= self.rows or y < 0:
            return chain

        if self.board[y][x] != Orbs.CLEARED and self.board[y][x] != color:
            return chain

        self.board[y][x] = Orbs.CLEARED

        right, _ = self._erase_orbs((x + 1, y), color, (chain[0] + 1, 0))
        _, down = self._erase_orbs((x, y + 1), color, (0, chain[1] + 1))

        if right < COMBO_LIMIT and down < COMBO_LIMIT:
            self.board[y][x] = color
            return chain

        return (right, down)
                        

    def _calc_combos(self) -> int:
        """
            Calculates the number of combos currently present on the board.
        """
        pass
    def __str__(self):
        
        string = ''
        for orb_rows in self.board:
            for orb in orb_rows:
                if orb is None:
                    string += 'empty '
                else:
                    string += f'{orb.name} '
            string += '\n'
        return string
