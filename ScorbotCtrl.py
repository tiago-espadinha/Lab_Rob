import pygame
import serial
import time
import numpy as np

import ScorbotCom as scom
import ScorbotCtrl as sctrl
import CtrlMapping as ctrlmap

default_pos = ((1300, -11700, -5480, -10300, 2140),(5000, 100, 8000, 0, 0))
default_pos_cam1 = ((-860, -14850, -430, -27000, -2930),(3100, -540, 7900, -200, -480)) # Camera position to see robot
default_pos_cam2 = ((-300, -15720, -28440, -4050, -2720),(2980, -410, 2810, -540, -460)) # Camera position to see gelatin




# Movement step size
sensitivity_array = [10, 100, 500]
sensitivity = 1

deadzone = 0.5

def cmp(a, b):
    return (a > b) - (a < b)
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


# Get controller input
def get_event(joystick, serial_port, highlight_surface, image, cur_pos, count):
    global sensitivity
    next_pos = cur_pos
#    serial_rob1 = serial_port



    # Z axis movement
    if joystick.get_button(ctrlmap.ctrl_map_btn['L1']):
        print("L1 pressed")
        draw_highlight(highlight_surface, ctrlmap.map_position['L1'])
        scom.send_command_manual(serial_port, "eeeee\r")
        time.sleep(0.1)
    if joystick.get_button(ctrlmap.ctrl_map_btn['R1']):
        draw_highlight(highlight_surface, ctrlmap.map_position['R1'])
        scom.send_command_manual(serial_port, "33333\r")
        time.sleep(0.1)

    for event in pygame.event.get():
            # Keyboard input
            count += 1
            pressed = pygame.key.get_pressed()

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
            # TODO: Avoid spamming
            # TODO: Fix sensitivity
            # TODO: Fix movement limiters
            if event.type == pygame.JOYAXISMOTION:
                
                # right up
                # if joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_L_vert']) < -deadzone and joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_L_horz']) > deadzone:
                #     draw_highlight(highlight_surface, ctrlmap.map_position['Up'])
                #     draw_highlight(highlight_surface, ctrlmap.map_position['Right'])        
                #     next_pos[1][0] += sensitivity_array[sensitivity]
                #     next_pos[1][1] -= sensitivity_array[sensitivity]
                #     scom.update_pos(serial_port, next_pos, 'ALL')
                #     if scom.move_to_pos(serial_port) == 1:
                #         cur_pos = next_pos  

                # # right down
                # elif joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_L_vert']) > deadzone and joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_L_horz']) > deadzone:
                #     draw_highlight(highlight_surface, ctrlmap.map_position['Down'])
                #     draw_highlight(highlight_surface, ctrlmap.map_position['Right'])        
                #     next_pos[1][0] -= sensitivity_array[sensitivity]
                #     next_pos[1][1] -= sensitivity_array[sensitivity]
                #     scom.update_pos(serial_port, next_pos, 'ALL')
                #     if scom.move_to_pos(serial_port) == 1:
                #         cur_pos = next_pos

                # # left down
                # elif joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_L_vert']) > deadzone and joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_L_horz']) < -deadzone:
                #     draw_highlight(highlight_surface, ctrlmap.map_position['Down'])
                #     draw_highlight(highlight_surface, ctrlmap.map_position['Left'])        
                #     next_pos[1][0] -= sensitivity_array[sensitivity]
                #     next_pos[1][1] += sensitivity_array[sensitivity]
                #     scom.update_pos(serial_port, next_pos, 'ALL')
                #     if scom.move_to_pos(serial_port) == 1:
                #         cur_pos = next_pos
                
                # # left up
                # elif joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_L_vert']) < -deadzone and joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_L_horz']) < -deadzone:
                #     draw_highlight(highlight_surface, ctrlmap.map_position['Up'])
                #     next_pos[1][0] += sensitivity_array[sensitivity]
                #     # scom.update_pos(serial_port, next_pos, 'X')
                #     # if scom.move_to_pos(serial_port) == 1:
                #     #     cur_pos = next_pos
                #     # Diagonal movement
                #     #if joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_L_horz']) < -deadzone:
                #     draw_highlight(highlight_surface, ctrlmap.map_position['Left'])                       
                #         #draw_highlight(highlight_surface, ctrlmap.map_position['Up'])
                #         #next_pos[1][0] += sensitivity_array[sensitivity]
                #     next_pos[1][1] += sensitivity_array[sensitivity]
                #     scom.update_pos(serial_port, next_pos, 'ALL')
                #     if scom.move_to_pos(serial_port) == 1:
                #         cur_pos = next_pos


                # Left movement
                if joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_L_horz']) < -deadzone:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Left'])
                    scom.send_command(serial_port, "22222\r")    
                    # next_pos[1][1] += sensitivity_array[sensitivity]
                    # scom.update_pos(serial_port, next_pos, 'Y')
                    # if scom.move_to_pos(serial_port) == 1:
                    #     cur_pos = next_pos
                # Right movement
                if joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_L_horz']) > deadzone:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Right'])
                    scom.send_command(serial_port, "wwwww\r")
                # Up movement
                if joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_L_vert']) < -deadzone:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Up'])
                    scom.send_command_manual(serial_port, "11111\r")
                #Down movement
                if joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_L_vert']) > deadzone:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Down'])
                    scom.send_command_manual(serial_port, "qqqqq\r")
                
                # Pitch movement joint
                if joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_R_vert']) < -deadzone:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Triangle'])
                    scom.send_command(serial_port, "44444\r")
                    # scom.get_position(serial_port)
                    # next_pos[0][3] += int(sensitivity_array[sensitivity]*10)
                    # scom.update_pos(serial_port, next_pos, '4', 'Joint')
                    # if scom.move_to_pos(serial_port) == 1:
                    #     cur_pos = next_pos

                if joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_R_vert']) > deadzone:
                    draw_highlight(highlight_surface, ctrlmap.map_position['X'])
                    scom.send_command(serial_port, "rrrrr\r")

                # Roll movement
                if joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_R_horz']) < -deadzone:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Square'])
                    scom.send_command_manual(serial_port, "tttttttttt\r")

                if joystick.get_axis(ctrlmap.ctrl_map_ax['Anlg_R_horz']) > deadzone:
                    draw_highlight(highlight_surface, ctrlmap.map_position['Circle'])
                    scom.send_command_manual(serial_port, "55555555555\r")

            # Button input
            if event.type == pygame.JOYBUTTONDOWN:


                scom.send_command(serial_port, "~\r")
                scom.receive_command(serial_port)
                scom.receive_command(serial_port)
                scom.receive_command(serial_port)

                cur_pos = scom.get_position(serial_port)


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
                    if serial_port is not None:
                        scom.send_command(serial_port, calib_com)
                        scom.receive_command(serial_port)
                        scom.receive_command(serial_port)   
                        scom.receive_command(serial_port)

                        #cur_pos = scom.get_position(serial_port)
                        # TODO: Check if robot recalibrated correctly
                    else:
                        print("Sent: " + calib_com)
                
                # Move to default position
                if joystick.get_button(ctrlmap.ctrl_map_btn['Circle']):             
                    draw_highlight(highlight_surface, ctrlmap.map_position['Circle'])
                    next_pos = list(list(item) for item in default_pos)
                    scom.update_pos(serial_port, next_pos, 'ALL')
                    if scom.move_to_pos(serial_port) == 1:
                        cur_pos = next_pos
                    else:
                        print("Movement Failed")

                # Initialize with current position
                if joystick.get_button(ctrlmap.ctrl_map_btn['X']):
                    draw_highlight(highlight_surface, ctrlmap.map_position['X']) 
                    cur_pos = scom.get_position(serial_port)
                    print ('Current position:' + str(cur_pos))

                #next_pos = cur_pos
                # X axis movement
                if joystick.get_button(ctrlmap.ctrl_map_btn['Up']):
                    draw_highlight(highlight_surface, ctrlmap.map_position['Up'])
                    next_pos[1][0] += sensitivity_array[sensitivity]
                    scom.update_pos(serial_port, next_pos, 'X')
                    if scom.move_to_pos(serial_port) == 1:
                        cur_pos = next_pos

                if joystick.get_button(ctrlmap.ctrl_map_btn['Down']):
                    draw_highlight(highlight_surface, ctrlmap.map_position['Down'])
                    next_pos[1][0] -= sensitivity_array[sensitivity]
                    scom.update_pos(serial_port, next_pos, 'X')
                    if scom.move_to_pos(serial_port) == 1:
                        cur_pos = next_pos

                # Y axis movement
                if joystick.get_button(ctrlmap.ctrl_map_btn['Left']):
                    draw_highlight(highlight_surface, ctrlmap.map_position['Left'])
                    next_pos[1][1] += sensitivity_array[sensitivity]
                    scom.update_pos(serial_port, next_pos, 'Y')
                    if scom.move_to_pos(serial_port) == 1:
                        cur_pos = next_pos

                if joystick.get_button(ctrlmap.ctrl_map_btn['Right']):
                    draw_highlight(highlight_surface, ctrlmap.map_position['Right'])
                    next_pos[1][1] -= sensitivity_array[sensitivity]
                    scom.update_pos(serial_port, next_pos, 'Y')
                    if scom.move_to_pos(serial_port) == 1:
                        cur_pos = next_pos
                
                # TODO: Clean code
                # TODO: Fix Image size
                if joystick.get_button(ctrlmap.ctrl_map_btn['Select']):
                    draw_highlight(highlight_surface, ctrlmap.map_position['Select'])
                    sensitivity = (sensitivity + 1) % 3
                    print("Sensitivity: " + str(sensitivity_array[sensitivity]))

                if joystick.get_button(ctrlmap.ctrl_map_btn['Start']):
                    draw_highlight(highlight_surface, ctrlmap.map_position['Start'])
                    # Load image
                    help_image_path = 'Images/PS3_ctrl_help.jpg'
                    help_image = pygame.image.load(help_image_path)
                    width, height = help_image.get_size()

                    screen = pygame.display.set_mode((width, height))
                    pygame.display.set_caption('Controller Help')
                    screen.blit(help_image, (0,0))
                    pygame.display.flip()
                    while True:
                        event2 = pygame.event.wait()
                        if event2.type == pygame.QUIT:
                            return True, cur_pos, count
                        elif event2.type == pygame.JOYBUTTONDOWN:
                            if joystick.get_button(ctrlmap.ctrl_map_btn['Start']):
                                # Close help screen
                                width, height = image.get_size()

                                screen = pygame.display.set_mode((width, height))
                                pygame.display.set_caption('Controller Mapper')
                                screen.blit(help_image, (0,0))
                                pygame.display.flip()
                                break#pygame.quit()
                scom.send_command_manual(serial_port, "~\r")


            # Clear Mapping Screen
            if event.type == pygame.KEYUP or event.type == pygame.JOYBUTTONUP:
                highlight_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)

            if event.type == pygame.QUIT:
                return True, cur_pos, count
    return False, cur_pos, count