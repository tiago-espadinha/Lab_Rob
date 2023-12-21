'''
Authors: 
    Diogo Rosa   - 93044
    Tomás Bastos - 93194
    Tiago Simões - 96329
'''

import pygame
import serial
import numpy as np
from Config import debug, pos_var, default_pos

# TODO: Check Manual Mode and Speed Profile
# TODO: Analyse Get Position and Move To Position errors

# Initialize serial port communication
def port_init(port_name):
    baud_rate = 9600
    try:
        serial_port = serial.Serial(port_name, baud_rate, timeout=1)
    except:
        print("Failed to connect to serial port.")

        if debug:
            return None
        else:
            exit(0)

    return serial_port


# Send command to serial port
def send_command(port, command):
    try:
        port.write(command.encode('utf8'))
    except:
        print("Failed to write to serial port.")
        return
    
    if debug:
        print("Sent: ", command.encode('utf8'))

    return
    

# Receive data from serial port
def receive_command(port):
    try:
        message = port.readline()
    except:
        print("Failed to read from serial port.")
        return None
    message = message.decode('utf8')

    if debug:
        print("Received: ", message)

    return message


# Send command to get current position
def get_position(serial_port):

    create_pos_com = "DEFP " + pos_var + "\r"
    save_pos_com = "HERE " + pos_var + "\r"
    read_pos_com = "LISTPV " + pos_var + "\r"

    if serial_port is not None:
        # Create variable to store position
        send_command(serial_port, create_pos_com)
        receive_command(serial_port)
        recv_com = receive_command(serial_port)

        # Save current position
        send_command(serial_port, save_pos_com)
        receive_command(serial_port)
        recv_com = receive_command(serial_port)

        if 'Done' in recv_com:
            # Get current coordinates
            send_command(serial_port, read_pos_com)
            receive_command(serial_port)
            recv_com = receive_command(serial_port)

            if 'Position' in recv_com:
                # Split string and save coordinates
                coord_array = np.zeros((2,5), dtype=int)
                
                recv_joint = receive_command(serial_port)
                recv_xyz = receive_command(serial_port)
                coord_joint = recv_joint.split(":")
                coord_xyz = recv_xyz.split(":")

                for j in range(1, 6):
                    aux_j = coord_joint[j][:-2]
                    aux_x = coord_xyz[j][:-2]
                    coord_array[0][j-1] = int(aux_j)
                    coord_array[1][j-1] = int(aux_x)
                return coord_array
                        
        print("Failed to get position.")
        return None
    
    # Debug mode
    elif debug:
        print("\nSent: " + create_pos_com)
        print("Sent: " + save_pos_com)
        print("Sent: " + read_pos_com + "\n")
        return list(list(item) for item in default_pos)


# Moves robot
def move_to_pos(serial_port):
    # Update final position
    move_com = "MOVE " + pos_var + "\r"
    
    if serial_port is not None:
        send_command(serial_port, move_com)
        receive_command(serial_port)
        recv_com = receive_command(serial_port)
        if not 'Done' in recv_com:
            print("Failed to move robot.")
            return 0
    
    # Debug mode
    elif debug:
        print("Sent: " + move_com)

    return 1

def move_to_home(serial_port):
    # Update final position
    move_com = "MOVE 0\r"
    
    if serial_port is not None:
        send_command(serial_port, move_com)
        receive_command(serial_port)
        recv_com = receive_command(serial_port)
        if not 'Done' in recv_com:
            print("Failed to move robot.")
            return 0
    
    # Debug mode
    elif debug:
        print("Sent: " + move_com)

    return 1



# Send command to update coordinates
def update_pos(serial_port, coord, axis, mode='XYZ'):
    if axis =='ALL':
        #if mode == 'XYZ':
            axis_arr = ['X', 'Y', 'Z', 'P', 'R']
            for i in range(len(axis_arr)):
                update_pos(serial_port, coord, axis_arr[i], mode)
        #elif mode == 'Joint':
            axis_arr = ['1', '2', '3', '4', '5']
            for i in range(len(axis_arr)):
                update_pos(serial_port, coord, axis_arr[i], mode)
    else:
        # With cartesian coordinates
        #if mode == 'XYZ':   
            if axis == 'X': # X-axis
                set_pos_com = "SETPVC " + pos_var + " X " + str(coord[1][0]) + "\r"
            if axis == 'Y': # Y-axis
                set_pos_com = "SETPVC " + pos_var + " Y " + str(coord[1][1]) + "\r"
            if axis == 'Z': # Z-axis
                set_pos_com = "SETPVC " + pos_var + " Z " + str(coord[1][2]) + "\r"
            if axis == 'P': # Pitch
                set_pos_com = "SETPVC " + pos_var + " P " + str(coord[1][3]) + "\r"
            if axis == 'R': # Roll
                set_pos_com = "SETPVC " + pos_var + " R " + str(coord[1][4]) + "\r"

        # With joint coordinates      
        #elif mode == 'Joint':
            if axis == '1': # Base
                set_pos_com = "SETPV " + pos_var + " 1 " + str(coord[0][0]) + "\r"
            if axis == '2': # Shoulder
                set_pos_com = "SETPV " + pos_var + " 2 " + str(coord[0][1]) + "\r"
            if axis == '3': # Elbow
                set_pos_com = "SETPV " + pos_var + " 3 " + str(coord[0][2]) + "\r"
            if axis == '4': # Wrist Pitch
                set_pos_com = "SETPV " + pos_var + " 4 " + str(coord[0][3]) + "\r"
            if axis == '5': # Wrist Roll
                set_pos_com = "SETPV " + pos_var + " 5 " + str(coord[0][4]) + "\r"

            if serial_port is not None:
                send_command(serial_port, set_pos_com)
                receive_command(serial_port)
                recv_com = receive_command(serial_port)
                if not 'Done' in recv_com:
                    print("Failed to update position.")

            # Debug mode
            elif debug:
                print("\nSent: " + set_pos_com)


# Toggle Manual Mode on/off
def toggle_manual(serial_port):
    send_command(serial_port, "~\r")
    receive_command(serial_port)
    receive_command(serial_port)
    receive_command(serial_port)
    return


# Change speed profile
def set_speed(serial_port, speed):

    send_command(serial_port, "SPEED " + str(speed) + "\r")
    receive_command(serial_port)
    receive_command(serial_port)
    
    return

# Highlight controller diagram
def draw_highlight(highlight_surface, position, input_type='button'):
    if input_type == 'button':
        highlight_color = (255, 255, 0) + (180,)
        highlight_radius = 25
    elif input_type == 'analog':
        highlight_color = (255, 0, 0)
        highlight_radius = 7
    pygame.draw.circle(highlight_surface, highlight_color, position, highlight_radius)

# Initialize controller
def controller_init():
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No gamepad found.")
        if debug:
            return None
        else:
            exit(0)
    
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    return joystick