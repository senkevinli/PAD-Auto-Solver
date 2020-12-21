# PAD Solver

> Auto Solver for GungHo's Puzzle and Dragons.

![Test](https://github.com/senkevinli/Pad-Auto-Solver/workflows/PAD_solver/badge.svg)

## Requirements
- An Android phone with Puzzles and Dragons installed.
- Linux system with root privileges.
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
  ### App Configurations
  - Select the 16:9 aspect ratio option in settings.
  - Select the normal orbs skin. Other orb skins are not supported currently.

