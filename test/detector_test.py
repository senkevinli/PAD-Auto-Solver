#!/usr/bin/env python3
import os
from src.solver.detector import detect
from src.solver.pad_types import Orbs
from PIL import Image

# Test if able to detect enhanced orbs. Uses fixtures.
def test_enhanced_detection():
    dirpath = os.path.join(os.path.dirname(__file__), 'fixtures/enhanced')

    dir = os.fsencode(dirpath)
    for file in os.listdir(dir):
        filename = os.fsdecode(file)
        
        with Image.open(os.path.join(dirpath, filename)) as img:

            # Make a list of a list since this is what `detect` needs.
            orb_list = [[img]]
            
            orb_type = filename[len('enhanced') + 1:-4].upper()
            assert detect(orb_list)[0][0] == Orbs[orb_type]

