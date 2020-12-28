# PAD Auto Solver

> Auto Solver for GungHo's Puzzle and Dragons.

![Test](https://github.com/senkevinli/Pad-Auto-Solver/workflows/Tests/badge.svg)

This is a command line interface tool that auto solves Puzzles and Dragon's boards on your connected phone. Currently only optimizes for combos (3+ connected orbs) and does not distinguish between solutions that have the same number of combos.
## Requirements
- An Android phone with Puzzles and Dragons installed.
- Linux system with root privileges, Python 3 and git installed.
- Must have Android Debug Bridge (ADB) installed. If not use:
    ```
    $ sudo apt-get update
    $ sudo apt install adb
    ```
- Start ADB on localhost port 5037 (this is the default) and connect your phone
  through USB to your PC. Set up your phone with Developer Options enabled. Instructions [here](https://wiki.lineageos.org/adb_fastboot_guide.html).
  
  To check if setup is correct, use:
  ```
  $ adb devices
  ```
  This should show your device's serial number with the name `device`.
  #### App Configurations
  - Select the 16:9 aspect ratio option in settings.
  - Select the normal orbs skin. Other orb skins are not supported currently.

## Setup

```
$ git clone https://github.com/senkevinli/PAD-Auto-Solver.git
$ cd PAD-Auto-Solver/
$ pip3 install .
$ pad_solver [options]
```

Use `pad_solver --help` for more options/configurations.
## Code Layout

#### `/src/solver/interface.py`

Device interface functionality exists here for screenshotting, setting coordinates for swipe inputs, and inputting swipes. Device inputs are piped into the phone through Android Debug Bridge with the help of [xiaocong/uiautomator](https://github.com/xiaocong/uiautomator). Board is found by using the dimensions of the phone screen and the dimensions of the app.

#### `src/solver/detector.py`

Orb detection happens here. Pillow images are converted to grayscale and then compared with PNG images in `src/references`. Comparison/feature matching of the Puzzles and Dragons orbs is completed through [ORB](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_orb/py_orb.html) detection (no pun intended) with the help of OpenCV.


#### `src/board.py`

Logic for board computations/simulating combos exists here. The only class method that mutates the layout of the boad is `move_orb` which swaps orb locations according to the specified parameters. Most of the other methods, including `calc_combos` preserves the original layout of the board.

#### `src/solver/solver.py`

Logic for actually solving the board exists here. Employs a naive greedy BFS or [Best-first search](https://en.wikipedia.org/wiki/Best-first_search)
to determine the best path for the optimal number of combos. Search begins on every possible starting coordinate of the board and is sorted by the number of combos first and the potential (how many more combos are possible) second.

Adjustments for sorting can be made in the `SolveState` less than method. The priority queue/min heap is fixed at a certain size to prevent long-running computations.

#### `tests/`

Simple pytest suite for verifying the functionality of the board and detector functionalities.
### TODO
- Rewrite logic for solving. Currently too slow and does not always produce optimal combos (6+).
- Improve testing suite to include tests for `src/solver/solver.py`.
- Find a better heuristic for erasing orbs in `src/solver/board.py` that does not include unnecessary computations.
- Add support for more orb types and other board dimensions
- Generalized approach for detecting the board that does not include phone screen computations.