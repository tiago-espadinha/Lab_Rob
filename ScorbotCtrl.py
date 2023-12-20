'''
Authors: 
    Diogo Rosa   - 93044
    Tomás Bastos - 93194
    Tiago Simões - 96329
'''

import pygame
import ScorbotCom as scom
from CtrlMapping import map_position, ctrl_map_btn, ctrl_map_ax
from variaveis import debug, default_pos, speed_array, speed_mode, deadzone

# TODO: Check if robot recalibrated correctly
# TODO: Have a mode Variable  
# TODO: Fix movement limiters

count = 0

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


# Get controller input
def get_event(joystick, highlight_surface, image):
    clr_flag = False
    from scorbot_ctrl import serial_cam, serial_scalp, serial_cur
    #import scorbot_ctrl as main
    global count
    if serial_cur == 'Cam':
        serial_port = serial_cam
    elif serial_cur == 'Scalp':
        serial_port = serial_scalp
    for event in pygame.event.get():
            count += 1
            
            # Analog input
            if event.type == pygame.JOYAXISMOTION:
                # X/Base movement 
                # Left
                if joystick.get_axis(ctrl_map_ax['Anlg_L_horz']) < -deadzone:
                    pos = (map_position['L3'][0]+(joystick.get_axis(ctrl_map_ax['Anlg_L_horz'])*30),map_position['L3'][1])
                    draw_highlight(highlight_surface, pos, 'analog')
                    if serial_port is not None:
                        scom.send_command(serial_port, "22222\r")

                # Right
                elif joystick.get_axis(ctrl_map_ax['Anlg_L_horz']) > deadzone:
                    pos = (map_position['L3'][0]+(joystick.get_axis(ctrl_map_ax['Anlg_L_horz'])*30),map_position['L3'][1])
                    draw_highlight(highlight_surface, pos, 'analog')
                    if serial_port is not None:
                        scom.send_command(serial_port, "wwwww\r")

                # Y/Shoulder movement
                # Forward
                elif joystick.get_axis(ctrl_map_ax['Anlg_L_vert']) < -deadzone:
                    pos = (map_position['L3'][0],map_position['L3'][1]+(joystick.get_axis(ctrl_map_ax['Anlg_L_vert'])*30))
                    draw_highlight(highlight_surface, pos, 'analog')
                    if serial_port is not None:
                        scom.send_command(serial_port, "11111\r")

                # Backward
                elif joystick.get_axis(ctrl_map_ax['Anlg_L_vert']) > deadzone:
                    pos = (map_position['L3'][0],map_position['L3'][1]+(joystick.get_axis(ctrl_map_ax['Anlg_L_vert'])*30))
                    draw_highlight(highlight_surface, pos, 'analog')
                    if serial_port is not None:
                        scom.send_command(serial_port, "qqqqq\r")
                
                # Z/Elbow movement
                # Up
                elif joystick.get_axis(ctrl_map_ax['Anlg_L2']) > deadzone:
                    draw_highlight(highlight_surface, map_position['L1'])
                    if serial_port is not None:
                        scom.send_command(serial_port, "eeeee\r")

                # Down
                elif joystick.get_axis(ctrl_map_ax['Anlg_R2']) > deadzone:
                    draw_highlight(highlight_surface, map_position['R1'])
                    if serial_port is not None:
                        scom.send_command(serial_port, "33333\r")

                # Pitch movement
                # Up
                elif joystick.get_axis(ctrl_map_ax['Anlg_R_vert']) < -deadzone:
                    pos = (map_position['R3'][0],map_position['R3'][1]+(joystick.get_axis(ctrl_map_ax['Anlg_R_vert'])*30))
                    draw_highlight(highlight_surface, pos, 'analog')
                    if serial_port is not None:
                        scom.send_command(serial_port, "44444\r")

                # Down
                elif joystick.get_axis(ctrl_map_ax['Anlg_R_vert']) > deadzone:
                    pos = (map_position['R3'][0],map_position['R3'][1]+(joystick.get_axis(ctrl_map_ax['Anlg_R_vert'])*30))
                    draw_highlight(highlight_surface, pos, 'analog')
                    if serial_port is not None:
                        scom.send_command(serial_port, "rrrrr\r")

                # Roll movement
                # Left
                elif joystick.get_axis(ctrl_map_ax['Anlg_R_horz']) < -deadzone:
                    pos = (map_position['R3'][0]+(joystick.get_axis(ctrl_map_ax['Anlg_R_horz'])*30), map_position['R3'][1])
                    draw_highlight(highlight_surface, pos, 'analog')
                    if serial_port is not None:
                        scom.send_command(serial_port, "tttt\r")

                # Right
                elif joystick.get_axis(ctrl_map_ax['Anlg_R_horz']) > deadzone:
                    pos = (map_position['R3'][0]+(joystick.get_axis(ctrl_map_ax['Anlg_R_horz'])*30), map_position['R3'][1])
                    draw_highlight(highlight_surface, pos, 'analog')
                    if serial_port is not None:
                        scom.send_command(serial_port, "5555\r")

            # Button input
            if event.type == pygame.JOYBUTTONDOWN:

                # Control Enable
                if joystick.get_button(ctrl_map_btn['L3']):
                    draw_highlight(highlight_surface, map_position['L3'])
                    if serial_port is not None:
                        scom.send_command(serial_port, "c\r")
                        scom.receive_command(serial_port)
                        scom.receive_command(serial_port)
                   
                # Joint/XYZ mode
                if joystick.get_button(ctrl_map_btn['R3']):
                    draw_highlight(highlight_surface, map_position['R3'])
                    if serial_port is not None:
                        mode = scom.receive_command(serial_port)
                        if 'JOINT' in mode:
                            scom.send_command(serial_port, "x\r")
                            scom.receive_command(serial_port)
                            scom.receive_command(serial_port)
                        else:    
                            scom.send_command(serial_port, "j\r")
                            scom.receive_command(serial_port)
                            scom.receive_command(serial_port)
                    
                # Speed
                if joystick.get_button(ctrl_map_btn['Select']):
                    draw_highlight(highlight_surface, map_position['Select'])
                    speed_mode = (speed_mode + 1) % 3
                    scom.set_speed(serial_port, speed_array[speed_mode])
                    print("Speed: " + str(speed_array[speed_mode]))

                # Switch Robots
                if joystick.get_button(ctrl_map_btn['Triangle']):
                    draw_highlight(highlight_surface, map_position['Triangle'])
                    if serial_cur == 'Cam':
                        serial_port = serial_cam
                        serial_cur = 'Scalp'
                        print("\nSwitched to Scalp")
                    elif serial_cur == 'Scalp':
                        serial_port = serial_scalp
                        serial_cur = 'Cam'
                        print("\nSwitched to Cam")

                # Exit manual mode
                if serial_port is not None:
                    scom.toggle_manual(serial_port)

                # Recalibrate
                if joystick.get_button(ctrl_map_btn['Square']):
                    draw_highlight(highlight_surface, map_position['Square'])
                    calib_com = "HOME\r"
                    if serial_port is not None:
                        scom.send_command(serial_port, calib_com)
                        scom.receive_command(serial_port)
                        scom.receive_command(serial_port)   
                        scom.receive_command(serial_port)
                        
                    else:
                        print("\nSent: " + calib_com)
                
                # Move to default position
                if joystick.get_button(ctrl_map_btn['Circle']):             
                    draw_highlight(highlight_surface, map_position['Circle'])
                    next_pos = list(list(item) for item in default_pos)
                    scom.update_pos(serial_port, next_pos, 'ALL')
                    if scom.move_to_pos(serial_port) != 1:
                        print("Return to Default Position Failed")

                # Get current position
                if joystick.get_button(ctrl_map_btn['X']):
                    draw_highlight(highlight_surface, map_position['X']) 
                    cur_pos = scom.get_position(serial_port)
                    if cur_pos is not None:
                        print ('Current position:' + str(cur_pos))
                    else:
                        print("Failed to get position.")
                
                # Show Help Screen
                if joystick.get_button(ctrl_map_btn['Start']):
                    draw_highlight(highlight_surface, map_position['Start'])
                    # Load image
                    help_image_path = 'Images/PS3_ctrl_help.jpg'
                    help_image = pygame.image.load(help_image_path)
                    width, height = help_image.get_size()

                    screen = pygame.display.set_mode((width, height))
                    pygame.display.set_caption('Controller Help')
                    screen.blit(help_image, (0,0))
                    pygame.display.flip()

                    # Wait for Start button to be pressed again
                    while True:
                        event2 = pygame.event.wait()
                        if event2.type == pygame.QUIT:
                            return True, clr_flag
                        elif event2.type == pygame.JOYBUTTONDOWN:
                            if joystick.get_button(ctrl_map_btn['Start']):
                                # Close help screen
                                width, height = image.get_size()

                                screen = pygame.display.set_mode((width, height))
                                pygame.display.set_caption('Controller Mapper')
                                screen.blit(help_image, (0,0))
                                pygame.display.flip()
                                break

                # Enter Manual Mode 
                if serial_port is not None:
                    scom.toggle_manual(serial_port)

            if event.type == pygame.JOYBUTTONUP: 
                clr_flag=True

            if event.type == pygame.QUIT:
                return True, clr_flag
    return False, clr_flag