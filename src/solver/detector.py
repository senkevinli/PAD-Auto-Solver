#!/usr/bin/env python3

import sys
import os
import cv2
import numpy as np

from matplotlib import pyplot as plt
from PIL import Image
from typing import List

from .pad_types import Orbs

CUR_DIR = os.path.dirname(__file__)
REFERENCE = os.path.join(CUR_DIR, '../references')

THRESHOLD = 20

def detect(
    raw_orbs: List[List[Image.Image]]
    ) -> List[List[Orbs]]:
    """
        Converts a list of Pillow Images into a List of
        Orbs. Detects colors using the least distance between
        two coordinate RGB points.
        TODO: Find a better heuristic for detecting colors.
    """
    orbs = []
    for row in raw_orbs:
        orb_row = []
        i = 0
        for orb in row:
            orb_rgb = orb.convert('RGB')
            converted = cv2.cvtColor(np.array(orb_rgb), cv2.COLOR_BGR2GRAY)
            
            orb_match = _match_img(converted)
            if (orb_match is not None):
                orb_row.append(orb_match)
            else:
                # Error happened with matching.
                return None
        orbs.append(orb_row)
    return orbs

def _debug_img(img: np.ndarray) -> Orbs:
    """
        Used for debugging. Shows cv2 image.
    """
    while True:
        try:
            cv2.imshow('window', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            break

def _match_img(img: np.ndarray) -> Orbs:
    """
        Matches a grayscale image with one of the
        .pngs in the specified folder.
    """
    dir = os.fsencode(REFERENCE)
    for file in os.listdir(dir):
        filename = os.fsdecode(file)
        
        # Only compares with other .pngs. Assumes
        # images are in grayscale.
        if filename.endswith('.png'):
            ref_img = cv2.imread(
                os.path.join(REFERENCE, filename),
                cv2.IMREAD_GRAYSCALE
            )

            # Following is taken/sligtly modified from OpenCV docs.

            # Initiate SIFT detector.
            orb = cv2.ORB_create()

            # Find keypoints and descriptors with SIFT.
            _, des1 = orb.detectAndCompute(ref_img, None)
            _, des2 = orb.detectAndCompute(img, None)

            # No features detected in query image, error.
            if des2 is None:
                return None
            
            # Continue if no features detected in reference image.
            if des1 is None:
                continue

            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)

            if len(matches) == 0:
                continue

            # Filter matches using specified threshold.
            matches = list(filter(lambda x: x.distance < THRESHOLD, matches))

            if len(matches) > 0:
                orb_type = filename[:-4].upper()
                return Orbs[orb_type]

    # No matches found, error.
    return None


