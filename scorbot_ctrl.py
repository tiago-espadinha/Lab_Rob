import pygame
import serial
import time
import numpy as np

import ScorbotCom as scom
import ScorbotCtrl as sctrl
import CtrlMapping as ctrlmap


def main():

    # Initialize serial port communication
    rob1_port = 'COM7'
    rob2_port = 'COM8'
    serial_rob1 = scom.port_init(rob1_port)
    serial_rob2 = scom.port_init(rob2_port)
    serial_port = serial_rob1

    # Initialize pygame and controller
    pygame.init()
    joystick = sctrl.controller_init()

    ### Button Layout ###
    # Load image
    image_path = 'Images/PS3_ctrl_layout.jpg'
    image = pygame.image.load(image_path)
    width, height = image.get_size()

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Controller Mapper')

    highlight_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)

    # Get controller input
    done = False
    while not done:
        done = sctrl.get_event(joystick, serial_port, highlight_surface, image)

        # Update controller window
        screen.blit(image, (0,0))
        screen.blit(highlight_surface,(0,0))
        pygame.display.flip()
        

if __name__ == '__main__':
    main()