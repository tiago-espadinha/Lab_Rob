# Scorbot Robot Project

## Introduction

This project provides a Python program that interfaces with two Scorbot robot, enabling control through a controller. 
The program is designed to facilitate robot movements and actions using the controller in order to perform an operation, with a robot holding a camera and the other a surgical scalp.

## Requirements

This project uses the following libraries:

* numpy
* opencv
* pygame
* pyserial
* time

## Usage

### Configuration

In the `Config.py` file make sure to adjust the following:

* scalp_port to the serial port assigned to the robot holding the scalp
* cam_port to the serial port assigned to the robot holding the camera
* cam_usb to the usb port assigned to the camera


### Running the Program

1. Connect a PS4 controller and the camera to the computer.

2. Connect both the robots to the serial port assigned in `Config.py` file.

3. Connect the camera to the usb port assigned in `Config.py` file.

4. Execute the program:

   ```bash
   python scorbot_run.py
   ``` 


### Recommendation

For a short and smooth operation it is suggested to begin by moving each robot to the default position, by pressing `Circle`

The help screen with the mapping of each button is available by pressing `Options`