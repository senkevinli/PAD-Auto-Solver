#!/usr/bin/env python3

""" Class for simulating/easing board computations """


from .pad_types import Orbs, Directions
from typing import List, Tuple
from copy import deepcopy
from pprint import pprint

COMBO_LIMIT = 3

def in_bounds(
    coord: Tuple[int, int],
    rows: int,
    cols: int
) -> bool:
    x, y = coord
    return x >= 0 and x < cols and y >= 0 and y < rows
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
                counts.update({orb: counts.get(orb, 0) + 1})
                copied_row.append([orb, False])
            copied.append(copied_row)

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
        self.board = copied
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
        right = go_right(coord, color)
        down = go_down(coord, color)
        
        print(right, down)
        sum = right + down
        if sum > 0:
            print(coord)
        # sum = go_right(coord, color) + go_down(coord, color)
        return sum

    def _erase_orbs2(
        self,
        coord: Tuple[int, int],
        color: Orbs,
        clusters,
        all_cleared
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
        if in_bounds((x + COMBO_LIMIT - 1, y), self.rows, self.cols):
            same = [ self.board[y][i][0] == color for i in range(x, x + COMBO_LIMIT) ]
            if all(same):
                for i in range(x, x + COMBO_LIMIT):
                    self.board[y][i][1] = True
                    changed.add((i, y))

        # Check down, only COMBO_LIMIT elements is enough.
        if in_bounds((x, y + COMBO_LIMIT - 1), self.rows, self.cols):
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
                for direction in Directions:
                    x2, y2 = tuple(
                        map(lambda src, change: src + change, (x,y), direction.value)
                    )
                    # Part of a cluster if orb to the up, left, right, and down
                    # is cleared and the same color.
                    if in_bounds((x2, y2), self.rows, self.cols) and \
                    self.board[y2][x2][1] == True and \
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
                    self._erase_orbs2((x, y), orb[0], clusters, all_cleared)
        
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
                string += '{:<15}'.format(orb[0])
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
