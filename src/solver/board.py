#!/usr/bin/env python3

""" Class for simulating/easing board computations """

from math import ceil
from .pad_types import Orbs, Directions
from typing import List, Tuple, Dict, Set
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

        # Make a copy for immutability
        copied = []

        for orb_row in orbs:
            copied_row = []
            for orb in orb_row:
                counts.update({orb[0]: counts.get(orb[0], 0) + 1})
                copied_row.append([orb[0], False])
            copied.append(copied_row)

        # Set private variables.
        self.board = copied
        self.rows = len(orbs)
        self.cols = len(orbs[0])
        self.counts = counts
        self.max = max
    
    def sub_cluster(self, clusters: Dict[Orbs, List[Set[Tuple[int, int]]]]) -> None:
        """
            Subtracts cluster from the colors count. Cluster can be obtained
            from `calc_combos`.
        """
        # Loop through colors and get the length.
        for color in clusters.keys():
            to_sub = 0

            # Subtract from clusters.
            for cluster in clusters.get(color):
                to_sub += len(cluster)
            self.counts.update({color: self.counts.get(color, 0) - to_sub})
    
    def get_potential(self) -> int:
        """
            Calculates the max number of combos possible from this board's
            counts.
        """
        # Constructive algorithm to calculate the max number of combos. Only
        # works for 6x5. There may be a better way to do this.
        # TODO: modify to account for 7x6 and 5x4 boards.
        max = 0
        exclude = None
        counts_copy = self.counts.copy()

        # Tracks how many combos per color. Sorting works because dictionary keeps
        # insertion order in Python 3.7+.
        sorted_dict = {k :v for k, v in 
                      sorted(self.counts.items(), key=lambda tup: tup[1], reverse=False)}

        free_spaces = self.rows * self.cols // COMBO_LIMIT
        combos = 0
        # Loop through sorted dict, largest color combo at the front.
        for color in sorted_dict:
            freq = sorted_dict.get(color)

            to_add = freq // COMBO_LIMIT
    
            # If orbs are the same color, cannot be adjacent, must be placed diagonally.
            # Thus, if we have more orbs than spaces to place them diagonally, we
            # need to subtract from combos.
            if freq > free_spaces // 2:

                # How many do we have left over. Subtract this will be adjacent to
                # our combos?
                diff = freq - free_spaces // 2
                
                if diff < COMBO_LIMIT:
                    pass
                if diff >= COMBO_LIMIT and diff < COMBO_LIMIT * 2:
                    to_add -= 2
                if diff == COMBO_LIMIT * 2:
                    to_add -= 3
                if diff > COMBO_LIMIT * 2 and diff < COMBO_LIMIT * 3:
                    to_add -= 5
                if diff == COMBO_LIMIT * 3:
                    to_add -= 6
                else:
                    to_add = 1

            combos += to_add
        return combos

    def in_bounds(self, coord: Tuple[int, int]) -> bool:
        """
            Returns true if coordinate is within bounds of the board.
        """
        x, y = coord
        return x >= 0 and x < self.cols and y >= 0 and y < self.rows

    def _erase_orbs(
        self,
        coord: Tuple[int, int],
        color: Orbs,
        clusters: Dict[Orbs, List[Set[Tuple[int, int]]]],
        all_cleared: Dict[Orbs, Set[Tuple[int, int]]]
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
        x, y = coord

        changed = set()
        # Check right first, only COMBO_LIMIT elements is enough.
        if self.in_bounds((x + COMBO_LIMIT - 1, y)):
            same = [ self.board[y][i][0] == color for i in range(x, x + COMBO_LIMIT) ]
            if all(same):
                for i in range(x, x + COMBO_LIMIT):
                    self.board[y][i][1] = True
                    changed.add((i, y))

        # Check down, only COMBO_LIMIT elements is enough.
        if self.in_bounds((x, y + COMBO_LIMIT - 1)):
            same = [ self.board[i][x][0] == color for i in range(y, y + COMBO_LIMIT)]
            if all(same):
                for i in range(y, y + COMBO_LIMIT):
                    self.board[i][x][1] = True
                    changed.add((x, i))

        # Were any changed?
        if len(changed) > 0:
            old_length = len(all_cleared.get(color))
            all_cleared.get(color).update(changed)

            if len(all_cleared.get(color)) > old_length:
                # If so, we may need to add to clusters.
                tgt_cluster = None        
                cluster_list = clusters.get(color)
                # Check if part of a cluster.
                for changes in changed:
                    x, y = changes
                    for direction in Directions:
                        x2, y2 = tuple(
                            map(lambda src, change: src + change, (x,y), direction.value)
                        )
                        # Part of a cluster if orb to the up, left, right, and down
                        # is cleared and the same color.
                        if self.in_bounds((x2, y2)) and \
                        self.board[y2][x2][1] and \
                        (x2, y2) in all_cleared.get(color):

                            for cluster in cluster_list:
                                if (x2, y2) in cluster:
                                    # Coalesce clusters.
                                    if tgt_cluster is not None and tgt_cluster is not cluster:
                                        tgt_cluster.update(cluster)
                                        cluster_list.remove(cluster)
                                    else:
                                        tgt_cluster = cluster
                
                if tgt_cluster is None:
                    tgt_cluster = set()
                    cluster_list.append(tgt_cluster)
            
                tgt_cluster.update(changed)

        return len(changed)

    def calc_combos(self) -> int:
        """
            Calculates the number of combos currently present on the board.
        """
        # Save current state because erase orbs will mutate the board.
        saved = deepcopy(self.board)

        # Key = color, value = list of sets of coordinates.
        clusters = { orb: [] for orb in Orbs if orb != Orbs.CLEARED}
        
        # For tracking the coordinates of everything has been cleared so far.
        all_cleared = { orb: set() for orb in Orbs if orb != Orbs.CLEARED }

        combos = 0
        for y, orb_row in enumerate(self.board):
            for x, orb in enumerate(orb_row):
                if (orb[0] != Orbs.CLEARED):
                    self._erase_orbs((x, y), orb[0], clusters, all_cleared)
        
        # Set orbs to `Cleared` now.
        need_recurse = False
        for orb_set in all_cleared.values():
            for coord in orb_set:
                need_recurse = True
                x, y = coord
                self.board[y][x] = [Orbs.CLEARED, False]

        # Stop if nothing was cleared.
        if not need_recurse:
            return 0, clusters

        # Simulate cascade.
        for x in range(self.cols):
            # `bound` is another pointer for this column.
            bound = self.rows - 1
            for y in range(self.rows - 1, -1, -1):
                # Populate if not `None`. Skip the other nones for now.
                if self.board[y][x][0] != Orbs.CLEARED:
                    self.board[bound][x] = self.board[y][x]
                    bound -= 1
            
            # Fill the rest of the space with `Cleared`
            for y in range(bound, -1, -1):
                self.board[y][x] = [Orbs.CLEARED, False]

        cascade_combos, cascade_clusters = self.calc_combos()

        # How many clusters for each cluster = how many combos.
        combos = sum([len(values) for values in clusters.values()]) + cascade_combos
        # Merge cascade clusters with our clusters.
        for color in clusters.keys():
            clusters.update({color: clusters.get(color) + cascade_clusters.get(color)})

        # Return board to original state.
        self.board = saved

        return combos, clusters
    
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
            Returns the board for duplication.
        """
        return self.board

    def __str__(self):
        """
            String representation used for debugging.
        """
        string = ''
        for orb_rows in self.board:
            for orb in orb_rows:
                if orb is None:
                    orb = 'EMPTY'
                string += '{:<15}'.format(orb[0])
            string += '\n'
        return string
