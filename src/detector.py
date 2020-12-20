#!/usr/bin/env python3

import sys
import cv2
import numpy as np

from functools import reduce
from math import sqrt
from PIL import Image
from typing import List
from pad_types import Orbs

def detect(
    raw_orbs: List[List[Image.Image]]
    ) -> List[List[Orbs]]:
    """
        Converts a list of Pillow Images into a List of
        Orbs. Detects colors using the least distance between
        two coordinate RGB points.
        TODO: Find a better heuristic for detecting colors.
    """

    # BGR dictionary for translating BGR values to a color.
    colors = {
        (108, 197, 59): Orbs.GREEN,
        (254, 204, 66): Orbs.BLUE,
        (177, 91, 241): Orbs.HEART,
        (174, 81, 169): Orbs.DARK,
        (73, 121, 254): Orbs.RED,
        (123, 243, 248): Orbs.LIGHT
    }

    orbs = []
    for row in raw_orbs:
        orb_row = []
        i = 0
        for orb in row:
            orb_delta = orb.convert('RGB')
            converted = cv2.cvtColor(np.array(orb_delta), cv2.COLOR_BGR2RGB)
            
            # Get BGR value of the center.
            dimensions = converted.shape
            width = dimensions[1] // 2
            height = dimensions[0] // 2
            
            b = converted[height, width, 0]
            g = converted[height, width, 1]
            r = converted[height, width, 2]
            
            # Euclidean distance to find nearest color.
            dist = sys.maxsize
            color = None

            for bgr in colors:
                diffs = tuple(map(lambda x, y: abs(x - y) ** 2, (b,g,r), bgr))
                temp_dist = sqrt(reduce(lambda x, y: x + y, diffs))
                if temp_dist < dist:
                    dist = temp_dist
                    color = colors.get(bgr)
            
            orb_row.append(color)
        
        orbs.append(orb_row)
    return orbs