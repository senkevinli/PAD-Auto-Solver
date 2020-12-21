#!/usr/bin/env python3

""" Class for simulating/easing board computations """


from .pad_types import Orbs, Directions
from typing import List, Tuple

class Board:
    def __init__(self, orbs: List[List[Orbs]]) -> None:
        """
            Initializes a board. Stores orbs as a numpy array.
            List must be a list of Orb enums.
        """

        # Get the orbs frequency.        
        counts = { orb: 0 for orb in Orbs}


        for orb_row in orbs:
            for orb in orb_row:
                counts.update({orb: counts.get(orb) + 1})
        print(counts)

        # Constructive algorithm to calculate the max number of combos. Only
        # works for 6x5.
        # TODO: modify to account for 7x6 and 5x4 boards.

        max = 0
        exclude = None
        counts_copy = counts.copy()
        while True:
            pruned = {k: v for k, v in counts_copy.items() if v >= 3}
            key_list = list(pruned.keys())

            if exclude is not None and len(key_list) == 1 and key_list[0] == exclude:
                break
            print(exclude)
            # Get the next orb to be excluded and count the combo.
            exclude = next((orb for orb in key_list if orb != exclude), None)
            print(pruned)
            if exclude is None:
                break
            pruned.update({exclude: pruned.get(exclude) - 3})
            max += 1
            counts_copy = pruned

        # Set private variables.
        self.board = orbs
        self.rows = len(orbs)
        self.cols = len(orbs[0])
        self.counts = counts
        self.max = max

    def _calc_combos(self) -> int:
        """
            Calculates the number of combos currently present on the board.
        """