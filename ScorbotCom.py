import pygame
import serial
import time
import numpy as np

import ScorbotCom as scom
import ScorbotCtrl as sctrl
import CtrlMapping as ctrlmap

pos_var = "A31"

# Initialize serial port communication
def port_init(port_name):
    baud_rate = 9600
    try:
        serial_port = serial.Serial(port_name, baud_rate, timeout=1)
    except:
        print("Failed to connect to serial port.")
        return None
    return serial_port


# Send command to serial port
def send_command(port, command):
    try:
        port.write(command.encode('utf8'))
    except:
        print("Failed to write to serial port.")
        return
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
    print("Recived: ", message)
    return message


# Send command to get current position
def get_position(serial_port):

    save_pos_com = "HERE " + pos_var + "\r"
    create_pos_com = "DEFP " + pos_var + "\r"
    read_pos_com = "LISTPV " + pos_var + "\r"

    if serial_port is not None:
        # Save current position
        send_command(serial_port, save_pos_com)
        receive_command(serial_port)
        recv_com = receive_command(serial_port)

        # Create variable if it doesn't exist
        if not 'Done' in recv_com:
            send_command(serial_port, create_pos_com)
            receive_command(serial_port)
            recv_com = receive_command(serial_port)

        # Get current coordinates
        if 'Done' in recv_com:
            send_command(serial_port, read_pos_com)
            receive_command(serial_port)
            recv_com = receive_command(serial_port)

            if 'Position' in recv_com:
                coord_array = np.zeros((2,5), dtype=int)
                for i in range(2):
                    recv_com = receive_command(serial_port)
                    coord_split = recv_com.split("   ")

                    # Split string and save coordinates
                    for j in range(5):
                        aux = coord_split[j].split(":")
                        coord_array[i][j] = int(aux[1])
                    return coord_array
                        
        print("Failed to get position.")
        return None
    
    # Debug mode
    else:
        print("\nSent: " + save_pos_com)
        print("Sent: " + create_pos_com)
        print("Sent: " + read_pos_com + "\n")
        return sctrl.default_pos

# Moves robot
def move_to_pos(serial_port):
    # Update final position
    move_com = "MOVE " + pos_var + "\r"
    
    if serial_port is not None:
        send_command(serial_port, move_com)
        receive_command(serial_port)
        recv_com = receive_command(serial_port)
        # TODO: Check if robot moved correctly
    
    # Debug mode
    else:
        print("Sent: " + move_com)

    return 1

# Send command to update coordinates
def update_pos(serial_port, coord, axis, mode='XYZ'):
    if axis =='ALL':
        if mode == 'XYZ':
            axis_arr = ['X', 'Y', 'Z', 'P', 'R']
            for i in range(len(axis_arr)):
                update_pos(serial_port, coord, axis_arr[i], mode)
        elif mode == 'Joint':
            axis_arr = ['1', '2', '3', '4', '5']
            for i in range(len(axis_arr)):
                update_pos(serial_port, coord, axis_arr[i], mode)
    else:
        # With cartesian coordinates
        if mode == 'XYZ':   
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
        elif mode == 'Joint':
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
            # TODO: Check if position was set correctly

        # Debug mode
        else:
            print("Sent: " + set_pos_com)
