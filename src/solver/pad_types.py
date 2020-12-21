""" Contains basic typing for orbs and movements. """

from enum import Enum
from enum import unique

@unique
class Orbs(Enum):
    """
        Orb types for PAD. Currently does not support Poison, Jammers,
        or any other types.
    """
    LIGHT = 0
    DARK = 1
    GREEN = 2
    RED = 3
    BLUE = 4
    HEART = 5

    CLEARED = 6

@unique
class Directions(Enum):
    """
        Direction enums for board movements. Diagonal movements not implemented.
        Value is a tuple (dx, dy).
    """
    LEFT = (-1, 0)
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)