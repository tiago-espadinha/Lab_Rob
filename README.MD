# Scorbot Robot Project

## Introduction

This project provides a Python program that interfaces with two Scorbot robot, enabling control through a controller. 
The program is designed to facilitate robot movements and actions using the controller in order to perform an operation, with a robot holding a camera and the other a surgical scalp.

## Prerequisites

This project uses the following libraries:

- pygame
- pyserial

## Usage

### Configuration

In the `Config.py` file adjust the serial port names to the ones available.


### Running the Program

1. Connect a PS4 controller and the camera to the computer.

2. Connect both the robots to the serial port assigned in `Config.py` file.

3. Execute the program:

   ```bash
   python scorbot_ctrl.py
   ``` 


### Recommendation

For a smooth operation it is suggested to begin by moving each robot to the default position, by pressing `Circle`

The help screen with the mapping of each button is available by pressing `Start`