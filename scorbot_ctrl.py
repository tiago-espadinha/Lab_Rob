'''
Authors: 
    Diogo Rosa   - 93044
    Tomás Bastos - 93194
    Tiago Simões - 96329
'''

import pygame
import ScorbotCom as scom
import ScorbotCtrl as sctrl
from Config import cam_port, scalp_port, speed_array, speed_mode

# TODO: Avoid double initialization
# TODO: Check Manual Mode and Robot initialization

# Initialize serial port communication
serial_cam = scom.port_init(cam_port)
serial_scalp = scom.port_init(scalp_port)
serial_cur = 'Cam'

def main():
    global serial_cam, serial_scalp, serial_cur

    # Initialize pygame and controller
    pygame.init()
    joystick = sctrl.controller_init()

    # Load image
    image_path = 'Images/PS3_ctrl_layout.jpg'
    image = pygame.image.load(image_path)
    width, height = image.get_size()

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Controller Mapper')

    highlight_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)

    # Initialize robot 1
    serial_port = serial_cam
    serial_cur = 'Cam'

    if serial_port is not None:
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

        # Initialize position
        
        scom.send_command(serial_port, "~\r")
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)

        scom.set_speed(serial_port, speed_array[speed_mode])

        scom.send_command(serial_port, "x\r")
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)


        scom.send_command(serial_port, "c\r")
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)

    #initialize robot 2
    serial_port = serial_scalp
    serial_cur = 'Scalp'

    if serial_port is not None:
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
        
        scom.send_command(serial_port, "~\r")
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)

        scom.set_speed(serial_port, speed_array[speed_mode])

        # Control enable
        scom.send_command(serial_port, "c\r")
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)

        # Toggle XYZ mode
        scom.send_command(serial_port, "x\r")
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)

    serial_port = serial_cam
    serial_cur = 'Cam'

    # Get controller input
    done = False
    while not done:
        done, clr_screen = sctrl.get_event(joystick, highlight_surface, image)

        # Update controller window
        if clr_screen:
                highlight_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        screen.blit(image, (0,0))
        screen.blit(highlight_surface,(0,0))
        pygame.display.flip()
        

if __name__ == '__main__':
    main()