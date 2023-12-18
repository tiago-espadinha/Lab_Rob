import pygame
import serial
import time
import numpy as np
import pyautogui

import ScorbotCom as scom
import ScorbotCtrl as sctrl
import CtrlMapping as ctrlmap

def main():

    # Initialize serial port communication
    rob1_port = 'COM3'
    rob2_port = 'COM4'
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

    # Default position [[Base, Shoulder, Elbow, Wrist Pitch, Wrist Roll][X, Y, Z, P, R]]
    default_pos = ((0, 0, 0, 0, 0),(5000, 100, 8000, 0, 0))
    cur_pos = list(list(item) for item in default_pos)


     # Initialize robot
    
    scom.send_command(serial_port, "CON\r")
    scom.receive_command(serial_port)
    scom.receive_command(serial_port)


    scom.send_command(serial_port, "~\r")
    scom.receive_command(serial_port)
    recv_com = scom.receive_command(serial_port)
    scom.receive_command(serial_port)
    
    if recv_com == "MANUAL MODE!\r\n":
        scom.send_command(serial_port, "~\r")
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)



    # # Initialize position
    cur_pos = scom.get_position(serial_port)
    print ('Current position:' + str(cur_pos))
    
    scom.send_command_manual(serial_port, "~\r")
    scom.receive_command(serial_port)
    scom.receive_command(serial_port)
    scom.receive_command(serial_port)

    scom.send_command(serial_port, "s\r")
    scom.receive_command(serial_port)

    scom.send_command(serial_port, "20\r")
    scom.receive_command(serial_port)
    scom.receive_command(serial_port)

    scom.send_command(serial_port, "x\r")
    scom.receive_command(serial_port)
    scom.receive_command(serial_port)


    scom.send_command_manual(serial_port, "c\r")
    scom.receive_command(serial_port)
    scom.receive_command(serial_port)

    #scom.send_command(serial_port, "CON\r")
    # scom.receive_command(serial_port)
    # scom.receive_command(serial_port)

    #manual mode
    # scom.send_command(serial_port, "~\r")
    # scom.receive_command(serial_port)
    
    # recv_com = scom.receive_command(serial_port)
    # if recv_com != "MANUAL MODE!\r\n":
    #     scom.send_command(serial_port, "~\r")
    #     scom.receive_command(serial_port)
    #     recv_com = scom.receive_command(serial_port)     
    # scom.receive_command(serial_port)
    # scom.receive_command(serial_port)
    # scom.send_command(serial_port, "s\r")
    # scom.send_command(serial_port, "35\r")
    # scom.receive_command(serial_port)
    # scom.receive_command(serial_port)
    # scom.send_command(serial_port, "c\r")
    # scom.receive_command(serial_port)
    # scom.receive_command(serial_port)


    # Get controller input
    done = False
    count = 0
    while not done:
        done, cur_pos, count = sctrl.get_event(joystick, serial_port, highlight_surface, image, cur_pos, count)
        # TODO: Fix screen update
        # Update controller window
        screen.blit(image, (0,0))
        screen.blit(highlight_surface,(0,0))
        pygame.display.flip()
        

if __name__ == '__main__':
    main()