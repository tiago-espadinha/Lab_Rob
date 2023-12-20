'''
Authors: 
    Diogo Rosa   - 93044
    Tomás Bastos - 93194
    Tiago Simões - 96329
'''

import pygame
import time
import ScorbotCom as scom
from CtrlMapping import map_position, ctrl_map_btn, ctrl_map_ax
from Config import debug, default_pos, speed_array, deadzone
import Config as cfg

# TODO: Check if robot recalibrated correctly
# TODO: Fix movement limiters

count = 0

# # Highlight controller diagram
# def scom.draw_highlight(highlight_surface, position, input_type='button'):
#     if input_type == 'button':
#         highlight_color = (255, 255, 0) + (180,)
#         highlight_radius = 25
#     elif input_type == 'analog':
#         highlight_color = (255, 0, 0)
#         highlight_radius = 7
#     pygame.draw.circle(highlight_surface, highlight_color, position, highlight_radius)


# # Initialize controller
# def controller_init():
#     pygame.joystick.init()

#     if pygame.joystick.get_count() == 0:
#         print("No gamepad found.")
#         if debug:
#             return None
#         else:
#             exit(0)
    
#     joystick = pygame.joystick.Joystick(0)
#     joystick.init()
#     return joystick


# # Get controller input
# def get_event(joystick, highlight_surface, image):
#     clr_flag = False
#     import scorbot_ctrl as main
#     from scorbot_ctrl import serial_cam, serial_scalp
#     screen_text = [pygame.font.SysFont("moonspace",24).render("Mode: " + main.joint_mode[main.serial_cur],1,(0,180,200)), 
#                    pygame.font.SysFont("moonspace",24).render("Robot: " + main.serial_cur,1,(0,180,200)),
#                    pygame.font.SysFont("moonspace",24).render("Speed: " + str(speed_array[cfg.speed_mode[main.serial_cur]]),1,(0,180,200))]
#     global count
#     if main.serial_cur == 'Cam':
#         serial_port = serial_cam
#     elif main.serial_cur == 'Scalp':
#         serial_port = serial_scalp
#     for event in pygame.event.get():
#             count += 1
            
#             # Analog input
#             if event.type == pygame.JOYAXISMOTION:
#                 # X/Base movement 
#                 # Left
#                 if joystick.get_axis(ctrl_map_ax['Anlg_L_horz']) < -deadzone:
#                     pos = (map_position['L3'][0]+(joystick.get_axis(ctrl_map_ax['Anlg_L_horz'])*30),map_position['L3'][1])
#                     scom.draw_highlight(highlight_surface, pos, 'analog')
#                     if serial_port is not None:
#                         scom.send_command(serial_port, "22222\r")

#                 # Right
#                 elif joystick.get_axis(ctrl_map_ax['Anlg_L_horz']) > deadzone:
#                     pos = (map_position['L3'][0]+(joystick.get_axis(ctrl_map_ax['Anlg_L_horz'])*30),map_position['L3'][1])
#                     scom.draw_highlight(highlight_surface, pos, 'analog')
#                     if serial_port is not None:
#                         if main.joint_mode[main.serial_cur] == 'JOINT':
#                             if cur_est[0][0] < cfg.limits_joint[0][1]:
#                                 scom.send_command(serial_port, "wwwww\r")
#                                 cur_est[0][0] += 100

#                 # Y/Shoulder movement
#                 # Forward
#                 elif joystick.get_axis(ctrl_map_ax['Anlg_L_vert']) < -deadzone:
#                     pos = (map_position['L3'][0],map_position['L3'][1]+(joystick.get_axis(ctrl_map_ax['Anlg_L_vert'])*30))
#                     scom.draw_highlight(highlight_surface, pos, 'analog')
#                     if serial_port is not None:
#                         scom.send_command(serial_port, "11111\r")

#                 # Backward
#                 elif joystick.get_axis(ctrl_map_ax['Anlg_L_vert']) > deadzone:
#                     pos = (map_position['L3'][0],map_position['L3'][1]+(joystick.get_axis(ctrl_map_ax['Anlg_L_vert'])*30))
#                     scom.draw_highlight(highlight_surface, pos, 'analog')
#                     if serial_port is not None:
#                         scom.send_command(serial_port, "qqqqq\r")
                
#                 # Z/Elbow movement
#                 # Up
#                 elif joystick.get_axis(ctrl_map_ax['Anlg_L2']) > deadzone:
#                     scom.draw_highlight(highlight_surface, map_position['L1'])
#                     if serial_port is not None:
#                         scom.send_command(serial_port, "eeeee\r")

#                 # Down
#                 elif joystick.get_axis(ctrl_map_ax['Anlg_R2']) > deadzone:
#                     scom.draw_highlight(highlight_surface, map_position['R1'])
#                     if serial_port is not None:
#                         scom.send_command(serial_port, "33333\r")

#                 # Pitch movement
#                 # Up
#                 elif joystick.get_axis(ctrl_map_ax['Anlg_R_vert']) < -deadzone:
#                     pos = (map_position['R3'][0],map_position['R3'][1]+(joystick.get_axis(ctrl_map_ax['Anlg_R_vert'])*30))
#                     scom.draw_highlight(highlight_surface, pos, 'analog')
#                     if serial_port is not None:
#                         scom.send_command(serial_port, "44444\r")

#                 # Down
#                 elif joystick.get_axis(ctrl_map_ax['Anlg_R_vert']) > deadzone:
#                     pos = (map_position['R3'][0],map_position['R3'][1]+(joystick.get_axis(ctrl_map_ax['Anlg_R_vert'])*30))
#                     scom.draw_highlight(highlight_surface, pos, 'analog')
#                     if serial_port is not None:
#                         scom.send_command(serial_port, "rrrrr\r")

#                 # Roll movement
#                 # Left
#                 elif joystick.get_axis(ctrl_map_ax['Anlg_R_horz']) < -deadzone:
#                     pos = (map_position['R3'][0]+(joystick.get_axis(ctrl_map_ax['Anlg_R_horz'])*30), map_position['R3'][1])
#                     scom.draw_highlight(highlight_surface, pos, 'analog')
#                     if serial_port is not None:
#                         scom.send_command(serial_port, "tttt\r")

#                 # Right
#                 elif joystick.get_axis(ctrl_map_ax['Anlg_R_horz']) > deadzone:
#                     pos = (map_position['R3'][0]+(joystick.get_axis(ctrl_map_ax['Anlg_R_horz'])*30), map_position['R3'][1])
#                     scom.draw_highlight(highlight_surface, pos, 'analog')
#                     if serial_port is not None:
#                         scom.send_command(serial_port, "5555\r")

#             # Button input
#             if event.type == pygame.JOYBUTTONDOWN:

#                 # Control Enable
#                 if joystick.get_button(ctrl_map_btn['L3']):
#                     scom.draw_highlight(highlight_surface, map_position['L3'])
#                     if serial_port is not None:
#                         scom.send_command(serial_port, "c\r")
#                         scom.receive_command(serial_port)
#                         scom.receive_command(serial_port)
                   
#                 # Joint/XYZ mode
#                 if joystick.get_button(ctrl_map_btn['R3']):
#                     scom.draw_highlight(highlight_surface, map_position['R3'])
#                     if main.joint_mode[main.serial_cur] == 'JOINT':
#                         if serial_port is not None:
#                             scom.send_command(serial_port, "x\r")
#                             scom.receive_command(serial_port)
#                             scom.receive_command(serial_port)
#                         main.joint_mode[main.serial_cur] = 'XYZ'
#                         print(main.serial_cur + " in XYZ Mode")

#                     elif main.joint_mode[main.serial_cur] == 'XYZ':
#                         if serial_port is not None:    
#                             scom.send_command(serial_port, "j\r")
#                             scom.receive_command(serial_port)
#                             scom.receive_command(serial_port)
#                         main.joint_mode[main.serial_cur] = 'JOINT'
#                         print(main.serial_cur + " in Joint Mode")

#                     #screen_text[0] = pygame.font.SysFont("moonspace",24).render("Mode: "+main.joint_mode[main.serial_cur],1,(255,0,0))
                    
#                 # Speed
#                 if joystick.get_button(ctrl_map_btn['Select']):
#                     scom.draw_highlight(highlight_surface, map_position['Select'])
#                     cfg.speed_mode[main.serial_cur] = (cfg.speed_mode[main.serial_cur] + 1) % 3
#                     scom.set_speed(serial_port, speed_array[cfg.speed_mode[main.serial_cur]])
#                     print("Speed: " + str(speed_array[cfg.speed_mode[main.serial_cur]]))

#                 # Switch Robots
#                 if joystick.get_button(ctrl_map_btn['Triangle']):
#                     scom.draw_highlight(highlight_surface, map_position['Triangle'])
#                     if main.serial_cur == 'Cam':
#                         serial_port = serial_cam
#                         main.serial_cur = 'Scalp'
#                         print("\nSwitched to Scalp")
#                     elif main.serial_cur == 'Scalp':
#                         serial_port = serial_scalp
#                         main.serial_cur = 'Cam'
#                         print("\nSwitched to Cam")
#                     #screen_text[1] = pygame.font.SysFont("moonspace",24).render("Robot: "+main.serial_cur,1,(255,0,0))

#                 # Exit manual mode
#                 if serial_port is not None:
#                     scom.toggle_manual(serial_port)

#                 # Recalibrate
#                 if joystick.get_button(ctrl_map_btn['Square']):
#                     scom.draw_highlight(highlight_surface, map_position['Square'])
#                     calib_com = "HOME\r"
#                     if serial_port is not None:
#                         scom.send_command(serial_port, calib_com)
#                         scom.receive_command(serial_port)
#                         scom.receive_command(serial_port)

#                         start_time = time.time()
#                         while True:
#                             recv_com = scom.receive_command(serial_port)
#                             if "Homing Complete" in recv_com:
#                                 print("Received :", recv_com)
#                                 break
#                             if time.time() - start_time > 180:
#                                 print("Homing Timeout")
#                                 break
                        
#                     else:
#                         print("\nSent: " + calib_com)
                
#                 # Move to default position
#                 if joystick.get_button(ctrl_map_btn['Circle']):             
#                     scom.draw_highlight(highlight_surface, map_position['Circle'])
#                     next_pos = list(list(item) for item in default_pos)
#                     scom.update_pos(serial_port, next_pos, 'ALL')
#                     if scom.move_to_pos(serial_port) != 1:
#                         print("Return to Default Position Failed")

#                 # Get current position
#                 if joystick.get_button(ctrl_map_btn['X']):
#                     scom.draw_highlight(highlight_surface, map_position['X']) 
#                     cur_pos = scom.get_position(serial_port)
#                     if cur_pos is not None:
#                         print ('Current position:' + str(cur_pos))
#                     else:
#                         print("Failed to get position.")
                
#                 # Show Help Screen
#                 if joystick.get_button(ctrl_map_btn['Start']):
#                     scom.draw_highlight(highlight_surface, map_position['Start'])
#                     # Load image
#                     help_image_path = 'Images/PS3_ctrl_help.jpg'
#                     help_image = pygame.image.load(help_image_path)
#                     width, height = help_image.get_size()

#                     help_screen = pygame.display.set_mode((width, height))
#                     pygame.display.set_caption('Controller Help')
#                     help_screen.blit(help_image, (0,0))
#                     pygame.display.flip()

#                     # Wait for Start button to be pressed again
#                     while True:
#                         event2 = pygame.event.wait()
#                         if event2.type == pygame.QUIT:
#                             return True, clr_flag, screen_text
#                         elif event2.type == pygame.JOYBUTTONDOWN:
#                             if joystick.get_button(ctrl_map_btn['Start']):
#                                 # Close help screen
#                                 width, height = image.get_size()

#                                 help_screen = pygame.display.set_mode((width, height))
#                                 pygame.display.set_caption('Controller Mapper')
#                                 help_screen.blit(help_image, (0,0))
#                                 pygame.display.flip()
#                                 break

#                 # Enter Manual Mode 
#                 if serial_port is not None:
#                     scom.toggle_manual(serial_port)

#             if event.type == pygame.JOYBUTTONUP: 
#                 clr_flag=True

#             if event.type == pygame.QUIT:
#                 return True, clr_flag, screen_text
#     return False, clr_flag, screen_text