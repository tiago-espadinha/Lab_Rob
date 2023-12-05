import pygame
import serial
import time
import numpy as np

import ScorbotCom as scom
import ScorbotCtrl as sctrl
import CtrlMapping as ctrlmap

speed = 10
# Default position [[Base, Shoulder, Elbow, Wrist Pitch, Wrist Roll][X, Y, Z, P, R]]
default_pos = [[0, 0, 0, 0, 0][5000, 100, 8000, 0, 0]]
cur_pos = default_pos
# Commands
speed_com = "SPEED " + str(speed)
default_com = "HERE " + str(default_pos)
teach_com = "TEACH "
list_com = "LISTPV A31\r"
del_com = "DELP A31"
here_com = "HERE A32\r"


# Highlight controller diagram
def draw_highlight(highlight_surface, position):
    highlight_color = (255, 255, 0) + (180,)
    highlight_radius = 25
    pygame.draw.circle(highlight_surface, highlight_color, position, highlight_radius)


# Initialize controller
def controller_init():
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No gamepad found.")
        return
    
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    return joystick


def get_event(joystick, serial_port, highlight_surface, image):
    for event in pygame.event.get():
            # Keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == ctrlmap.ctrl_map_key['Triangle']:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Triangle'])
                if event.key == ctrlmap.ctrl_map_key['Square']:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Square'])
                if event.key == ctrlmap.ctrl_map_key['Circle']:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Circle'])
                if event.key == ctrlmap.ctrl_map_key['X']:
                    draw_highlight(highlight_surface, ctrlmap.map_position['X'])

                if event.key == ctrlmap.ctrl_map_key['Up']:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Up'])
                if event.key == ctrlmap.ctrl_map_key['Down']:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Down'])
                if event.key == ctrlmap.ctrl_map_key['Left']:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Left'])
                if event.key == ctrlmap.ctrl_map_key['Right']:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Right'])
                    

                if event.key == ctrlmap.ctrl_map_key['L1']:
                    draw_highlight(highlight_surface, ctrlmap.map_position['L1'])
                if event.key == ctrlmap.ctrl_map_key['R1']:
                    draw_highlight(highlight_surface, ctrlmap.map_position['R1'])
                if event.key == ctrlmap.ctrl_map_key['L3']:
                    draw_highlight(highlight_surface, ctrlmap.map_position['L3'])
                if event.key == ctrlmap.ctrl_map_key['R3']:
                    draw_highlight(highlight_surface, ctrlmap.map_position['R3'])

                if event.key == ctrlmap.ctrl_map_key['Options']:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Options'])
                if event.key == ctrlmap.ctrl_map_key['Share']:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Share'])
                if event.key == ctrlmap.ctrl_map_key['PS']:
                    draw_highlight(highlight_surface, ctrlmap.map_position['PS'])
                if event.key == ctrlmap.ctrl_map_key['Touchpad']:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Touchpad'])
            
            # Controller input
            # Analog input
            if event.type == pygame.JOYAXISMOTION:
                
                next_pos = cur_pos

                # X axis movement
                if joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_L_vert']) < -0.5:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Up'])
                    next_pos[1][0] += 100
                    if scom.move_to_pos(serial_port, next_pos, 'X', serial_port) == 1:
                        cur_pos = next_pos
                    
                if joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_L_vert']) > 0.5:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Down'])
                    next_pos[1][0] -= 100
                    if scom.move_to_pos(serial_port, next_pos, 'X', serial_port) == 1:
                        cur_pos = next_pos

                # Y axis movement
                if joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_L_horz']) < -0.5:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Left'])
                    next_pos[1][1] += 100
                    if scom.move_to_pos(serial_port, next_pos, 'Y', serial_port) == 1:
                        cur_pos = next_pos

                if joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_L_horz']) > 0.5:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Right'])
                    next_pos[1][1] -= 100
                    if scom.move_to_pos(serial_port, next_pos, 'Y', serial_port) == 1:
                        cur_pos = next_pos

                # Pitch movement
                if joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_R_vert']) < -0.5:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Triangle'])
                    next_pos[1][3] += 50
                    if scom.move_to_pos(serial_port, next_pos, 'P', serial_port) == 1:
                        cur_pos = next_pos
                if joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_R_vert']) > 0.5:
                    draw_highlight(highlight_surface, ctrlmap.map_position['X'])
                    next_pos[1][3] -= 50
                    if scom.move_to_pos(serial_port, next_pos, 'P', serial_port) == 1:
                        cur_pos = next_pos

                # Roll movement
                if joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_R_horz']) < -0.5:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Square'])
                    next_pos[1][4] += 50
                    if scom.move_to_pos(serial_port, next_pos, 'R', serial_port) == 1:
                        cur_pos = next_pos
                if joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_R_horz']) > 0.5:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Circle'])
                    next_pos[1][4] -= 50
                    if scom.move_to_pos(serial_port, next_pos, 'R', serial_port) == 1:
                        cur_pos = next_pos


            # Button input
            if event.type == pygame.JOYBUTTONDOWN:
                # Switch Robots
                if joystick.get_button(ctrlmap.ctrl_map_btn['Triangle']):
                    draw_highlight(highlight_surface, ctrlmap.map_position['Triangle'])
                    # TODO: Implement switching correctly
                    # if serial_port == serial_rob1:
                    #     serial_port = serial_rob2
                    # else:
                    #     serial_port = serial_rob1

                # Recalibrate
                if joystick.get_button(ctrlmap.ctrl_map_btn['Square']):
                    draw_highlight(highlight_surface, ctrlmap.map_position['Square'])
                    calib_com = "HOME\r"
                    scom.send_command(serial_port, calib_com)
                    # TODO: Check if robot recalibrated correctly
                
                # Move to default position
                if joystick.get_button(ctrlmap.ctrl_map_btn['Circle']):             
                    draw_highlight(highlight_surface, ctrlmap.map_position['Circle'])
                    next_pos = default_pos
                    if scom.move_to_pos(serial_port, next_pos, 'XYZ', serial_port) == 1:
                        cur_pos = next_pos
                    else:
                        print("Movement Failed")

                # Initialize with current position
                if joystick.get_button(ctrlmap.ctrl_map_btn['X']):
                    draw_highlight(highlight_surface, ctrlmap.map_position['X']) 
                    cur_pos = scom.get_position(serial_port)
                    print ('Current position:' + str(cur_pos))

                next_pos = cur_pos
                # X axis movement
                if joystick.get_button(ctrlmap.ctrl_map_btn['Up']):
                    draw_highlight(highlight_surface, ctrlmap.map_position['Up'])
                    next_pos[1][0] += 100
                    if scom.move_to_pos(serial_port, next_pos, 'X', serial_port) == 1:
                        cur_pos = next_pos

                if joystick.get_button(ctrlmap.ctrl_map_btn['Down']):
                    draw_highlight(highlight_surface, ctrlmap.map_position['Down'])
                    next_pos[1][0] -= 100
                    if scom.move_to_pos(serial_port, next_pos, 'X', serial_port) == 1:
                        cur_pos = next_pos

                # Y axis movement
                if joystick.get_button(ctrlmap.ctrl_map_btn['Left']):
                    draw_highlight(highlight_surface, ctrlmap.map_position['Left'])
                    next_pos[1][1] += 100
                    if scom.move_to_pos(serial_port, next_pos, 'Y', serial_port) == 1:
                        cur_pos = next_pos

                if joystick.get_button(ctrlmap.ctrl_map_btn['Right']):
                    draw_highlight(highlight_surface, ctrlmap.map_position['Right'])
                    next_pos[1][1] -= 100
                    if scom.move_to_pos(serial_port, next_pos, 'Y', serial_port) == 1:
                        cur_pos = next_pos

                # Z axis movement
                if joystick.get_button(ctrlmap.ctrl_map_btn['L1']):
                    draw_highlight(highlight_surface, ctrlmap.map_position['L1'])
                    next_pos[1][2] -= 100
                    if scom.move_to_pos(serial_port, next_pos, 'Z', serial_port) == 1:
                        cur_pos = next_pos

                if joystick.get_button(ctrlmap.ctrl_map_btn['R1']):
                    draw_highlight(highlight_surface, ctrlmap.map_position['R1'])
                    next_pos[1][2] += 100
                    if scom.move_to_pos(serial_port, next_pos, 'Z', serial_port) == 1:
                        cur_pos = next_pos

            # Clear Mapping Screen
            if event.type == pygame.KEYUP or event.type == pygame.JOYBUTTONUP:
                highlight_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)

            if event.type == pygame.QUIT:
                return True
    return False