HoVR
====

A Blender Game Engine Demo for the Oculus Rift and the Nintendo Balance Board

## Hardware Requirements

* Oculus Rift (tested with DK1)
* Wii Balance Board
* Bluetooth dongle

## Dependencies

* python-rift 
  https://github.com/lubosz/python-rift
* python-balanceboard
  https://github.com/lubosz/python-balanceboard
* Blender 2.71
* udev rules for Oculus Rift on Linux

## Installation

If you are not on Arch Linux you need to build and install 4 packages manually.

* WiiC
* python-balanceboard
* OpenHMD
* python-rift

## Arch Linux Package

https://aur.archlinux.org/packages/hovr-git/

```
$ pacaur -S hovr-git
```

## Run Demo

1. Connect the Rift and setup a mirrored screen
2. Make sure your Bluetooth works and the Balance Board connects (wiic-example is a good test)
3. Open HoVR.blend in Blender
4. Press "P" in the Blender Viewer
5. Press the red connection button on your Balance Board

## Controls

* P: Start the Blender Game Engine
* R: Reset the in-game position and Rift orientation
* ESC: End Blender Game Engine

## Credits

includes sky shader based on implementation from 
Simon Wallner
http://www.simonwallner.at/

Water shader and scene by
Martins Upitis (martinsh) 
http://devlog-martinsh.blogspot.de/

VR, Input and physics

Lubosz Sarnecki

## Blog Post

http://lubosz.wordpress.com/2014/08/12/hovr-a-blender-game-engine-demo-for-the-oculus-rift-and-the-nintendo-balance-board/
