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
    print("Received: ", message)
    return message


# Send command to get current position
def get_position(serial_port):

    create_pos_com = "DEFP " + pos_var + "\r"
    save_pos_com = "HERE " + pos_var + "\r"
    read_pos_com = "LISTPV " + pos_var + "\r"

    if serial_port is not None:
        # TODO: Check order "DEFP", "HERE", "LISTPV"
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
                
                recv_com1 = receive_command(serial_port)
                recv_com2 = receive_command(serial_port)
                coord_split1 = recv_com1.split(":")
                coord_split2 = recv_com2.split(":")

                for j in range(1, 6):
                    aux1 = coord_split1[j][:-2]
                    aux2 = coord_split2[j][:-2]
                    coord_array[0][j-1] = int(aux1)
                    coord_array[1][j-1] = int(aux2)
                return coord_array
                        
        print("Failed to get position.")
        return None
    
    # Debug mode
    else:
        print("\nSent: " + create_pos_com)
        print("Sent: " + save_pos_com)
        print("Sent: " + read_pos_com + "\n")
        return list(list(item) for item in sctrl.default_pos)

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
            if not 'Done' in recv_com:
                print("Failed to update position.")

        # Debug mode
        else:
            print("Sent: " + set_pos_com)
