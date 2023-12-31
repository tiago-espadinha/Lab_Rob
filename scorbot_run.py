'''
Authors: 
    Diogo Rosa   - 93044
    Tomás Bastos - 93194
    Tiago Simões - 96329
'''

import pygame
import ScorbotCom as scom
import Config as cfg
from Config import cam_port, scalp_port, cam_usb, speed_array, speed_mode, default_pos, deadzone, delta, debug
from CtrlMap import map_position, ctrl_map_btn, ctrl_map_ax
import time
import cv2

# Initialize serial port communication
serial_cam = scom.port_init(cam_port)
serial_scalp = scom.port_init(scalp_port)
serial_cur = 'Cam'
joint_mode = {'Cam': 'XYZ', 'Scalpel': 'XYZ'}
cur_est = {'Cam': [[0,0,0,0,0],[0,0,0,0,0]], 'Scalpel': [[0,0,0,0,0],[0,0,0,0,0]]}


# Get controller input
def get_event(joystick, highlight_surface, image):
    global serial_cur
    clr_flag = False
    screen_text = [pygame.font.SysFont("moonspace",30).render("Mode: " + joint_mode[serial_cur],1,(132, 86, 139)), 
                   pygame.font.SysFont("moonspace",30).render("Robot: " + serial_cur,1,(132, 86, 139)),
                   pygame.font.SysFont("moonspace",30).render("Speed: " + str(speed_array[cfg.speed_mode[serial_cur]]),1,(132, 86, 139))]
    if serial_cur == 'Cam':
        serial_port = serial_cam
    elif serial_cur == 'Scalpel':
        serial_port = serial_scalp
    for event in pygame.event.get():
            
            # Analog input
            if event.type == pygame.JOYAXISMOTION:
                # Y/Base movement 
                # Left
                if joystick.get_axis(ctrl_map_ax['Anlg_L_horz']) < -deadzone:
                    pos = (map_position['L3'][0]+(joystick.get_axis(ctrl_map_ax['Anlg_L_horz'])*30),map_position['L3'][1])
                    scom.draw_highlight(highlight_surface, pos, 'analog')
                    if serial_port is not None:
                        if joint_mode[serial_cur] == 'JOINT':
                            if cur_est[serial_cur][0][0] < cfg.limits_joint[0][0]:
                                scom.send_command(serial_port, "qq\r")
                                cur_est[serial_cur][0][0] += delta[cfg.speed_mode[serial_cur]][0][0]
                        if joint_mode[serial_cur] == 'XYZ':
                            if cur_est[serial_cur][1][1] < cfg.limits_xyz[1][1]:
                                scom.send_command(serial_port, "22\r")
                                cur_est[serial_cur][1][1] += delta[cfg.speed_mode[serial_cur]][1][1]
                # Right
                elif joystick.get_axis(ctrl_map_ax['Anlg_L_horz']) > deadzone:
                    pos = (map_position['L3'][0]+(joystick.get_axis(ctrl_map_ax['Anlg_L_horz'])*30),map_position['L3'][1])
                    scom.draw_highlight(highlight_surface, pos, 'analog')
                    if serial_port is not None:
                        if joint_mode[serial_cur] == 'JOINT':
                            if cur_est[serial_cur][0][0] > cfg.limits_joint[0][1]:
                                scom.send_command(serial_port, "11\r")
                                cur_est[serial_cur][0][0] -= delta[cfg.speed_mode[serial_cur]][0][0]
                        if joint_mode[serial_cur] == 'XYZ':
                            if cur_est[serial_cur][1][1] > cfg.limits_xyz[1][0]:
                                scom.send_command(serial_port, "ww\r")
                                cur_est[serial_cur][1][1] -= delta[cfg.speed_mode[serial_cur]][1][1]
                                
                # X/Shoulder movement
                # Forward
                elif joystick.get_axis(ctrl_map_ax['Anlg_L_vert']) < -deadzone:
                    pos = (map_position['L3'][0],map_position['L3'][1]+(joystick.get_axis(ctrl_map_ax['Anlg_L_vert'])*30))
                    scom.draw_highlight(highlight_surface, pos, 'analog')
                    if serial_port is not None:
                        if joint_mode[serial_cur] == 'JOINT':
                            if cur_est[serial_cur][0][1] > cfg.limits_joint[1][0]:
                                scom.send_command(serial_port, "22\r")
                                cur_est[serial_cur][0][1] -= delta[cfg.speed_mode[serial_cur]][0][1]

                        if joint_mode[serial_cur] == 'XYZ':
                            if cur_est[serial_cur][1][0] > cfg.limits_xyz[0][0]:
                                scom.send_command(serial_port, "11\r")
                                cur_est[serial_cur][1][0] -= delta[cfg.speed_mode[serial_cur]][1][0]


                # Backward
                elif joystick.get_axis(ctrl_map_ax['Anlg_L_vert']) > deadzone:
                    pos = (map_position['L3'][0],map_position['L3'][1]+(joystick.get_axis(ctrl_map_ax['Anlg_L_vert'])*30))
                    scom.draw_highlight(highlight_surface, pos, 'analog')
                    if serial_port is not None:
                        if joint_mode[serial_cur] == 'JOINT':
                            if cur_est[serial_cur][0][1] < cfg.limits_joint[1][1]:
                                scom.send_command(serial_port, "ww\r")
                                cur_est[serial_cur][0][1] += delta[cfg.speed_mode[serial_cur]][0][1]
                        if joint_mode[serial_cur] == 'XYZ':
                            if cur_est[serial_cur][1][0] < cfg.limits_xyz[0][1]:
                                scom.send_command(serial_port, "qq\r")
                                cur_est[serial_cur][1][0] += delta[cfg.speed_mode[serial_cur]][1][0]
                
                # Z/Elbow movement
                # Up
                elif joystick.get_axis(ctrl_map_ax['Anlg_L2']) > deadzone:
                    scom.draw_highlight(highlight_surface, map_position['L1'])
                    if serial_port is not None:
                        if joint_mode[serial_cur] == 'JOINT':
                            if cur_est[serial_cur][0][2] > cfg.limits_joint[2][0]:
                                scom.send_command(serial_port, "ee\r")
                                cur_est[serial_cur][0][2] -= delta[cfg.speed_mode[serial_cur]][0][2]
                        if joint_mode[serial_cur] == 'XYZ':
                            if cur_est[serial_cur][1][2] > cfg.limits_xyz[2][0]:
                                scom.send_command(serial_port, "ee\r")
                                cur_est[serial_cur][1][2] -= delta[cfg.speed_mode[serial_cur]][1][2]

                # Down
                elif joystick.get_axis(ctrl_map_ax['Anlg_R2']) > deadzone:
                    scom.draw_highlight(highlight_surface, map_position['R1'])
                    if serial_port is not None:
                        if joint_mode[serial_cur] == 'JOINT':
                            if cur_est[serial_cur][0][2] < cfg.limits_joint[2][1]:
                                scom.send_command(serial_port, "33\r")
                                cur_est[serial_cur][0][2] += delta[cfg.speed_mode[serial_cur]][0][2]
                        if joint_mode[serial_cur] == 'XYZ':
                            if cur_est[serial_cur][1][2] < cfg.limits_xyz[2][1]:
                                scom.send_command(serial_port, "33\r")
                                cur_est[serial_cur][1][2] += delta[cfg.speed_mode[serial_cur]][1][2]

                # Pitch movement
                # Up
                elif joystick.get_axis(ctrl_map_ax['Anlg_R_vert']) < -deadzone:
                    pos = (map_position['R3'][0],map_position['R3'][1]+(joystick.get_axis(ctrl_map_ax['Anlg_R_vert'])*30))
                    scom.draw_highlight(highlight_surface, pos, 'analog')
                    if serial_port is not None:
                        if joint_mode[serial_cur] == 'JOINT':
                            if cur_est[serial_cur][0][3] < cfg.limits_joint[3][1]:
                                scom.send_command(serial_port, "44\r")
                                cur_est[serial_cur][0][3] += delta[cfg.speed_mode[serial_cur]][0][3]
                        if joint_mode[serial_cur] == 'XYZ':
                            if cur_est[serial_cur][1][3] < cfg.limits_xyz[3][1]:
                                scom.send_command(serial_port, "44\r")
                                cur_est[serial_cur][1][3] += delta[cfg.speed_mode[serial_cur]][1][3]


                # Down
                elif joystick.get_axis(ctrl_map_ax['Anlg_R_vert']) > deadzone:
                    pos = (map_position['R3'][0],map_position['R3'][1]+(joystick.get_axis(ctrl_map_ax['Anlg_R_vert'])*30))
                    scom.draw_highlight(highlight_surface, pos, 'analog')
                    if serial_port is not None:
                        if joint_mode[serial_cur] == 'JOINT':
                            if cur_est[serial_cur][0][3] > cfg.limits_joint[3][0]:
                                scom.send_command(serial_port, "rr\r")
                                cur_est[serial_cur][0][3] -= delta[cfg.speed_mode[serial_cur]][0][3]
                        if joint_mode[serial_cur] == 'XYZ':
                            if cur_est[serial_cur][1][3] > cfg.limits_xyz[3][0]:
                                scom.send_command(serial_port, "rr\r")
                                cur_est[serial_cur][1][3] -= delta[cfg.speed_mode[serial_cur]][1][3]


                # Roll movement
                # Left
                elif joystick.get_axis(ctrl_map_ax['Anlg_R_horz']) < -deadzone:
                    pos = (map_position['R3'][0]+(joystick.get_axis(ctrl_map_ax['Anlg_R_horz'])*30), map_position['R3'][1])
                    scom.draw_highlight(highlight_surface, pos, 'analog')
                    if serial_port is not None:
                        scom.send_command(serial_port, "tt\r")

                # Right
                elif joystick.get_axis(ctrl_map_ax['Anlg_R_horz']) > deadzone:
                    pos = (map_position['R3'][0]+(joystick.get_axis(ctrl_map_ax['Anlg_R_horz'])*30), map_position['R3'][1])
                    scom.draw_highlight(highlight_surface, pos, 'analog')
                    if serial_port is not None:
                        scom.send_command(serial_port, "55\r")


            # Button input
            if event.type == pygame.JOYBUTTONDOWN:

                # Control Enable
                if joystick.get_button(ctrl_map_btn['L3']):
                    scom.draw_highlight(highlight_surface, map_position['L3'])
                    if serial_port is not None:
                        scom.send_command(serial_port, "c\r")
                        scom.receive_command(serial_port)
                        scom.receive_command(serial_port)
                   
                # Joint/XYZ mode
                if joystick.get_button(ctrl_map_btn['R3']):
                    scom.draw_highlight(highlight_surface, map_position['R3'])
                    if joint_mode[serial_cur] == 'JOINT':
                        if serial_port is not None:
                            scom.send_command(serial_port, "x\r")
                            scom.receive_command(serial_port)
                            scom.receive_command(serial_port)
                        joint_mode[serial_cur] = 'XYZ'
                        print(serial_cur + " in XYZ Mode")

                    elif joint_mode[serial_cur] == 'XYZ':
                        if serial_port is not None:    
                            scom.send_command(serial_port, "j\r")
                            scom.receive_command(serial_port)
                            scom.receive_command(serial_port)
                        joint_mode[serial_cur] = 'JOINT'
                        print(serial_cur + " in Joint Mode")

                    scom.toggle_manual(serial_port)
                    cur_est[serial_cur] = scom.get_position(serial_port)
                    scom.toggle_manual(serial_port)

                # Switch Robots
                if joystick.get_button(ctrl_map_btn['Triangle']):
                    scom.draw_highlight(highlight_surface, map_position['Triangle'])
                    if serial_cur == 'Cam':
                        serial_port = serial_cam
                        serial_cur = 'Scalpel'
                        print("\nSwitched to Scalpel")
                    elif serial_cur == 'Scalpel':
                        serial_port = serial_scalp
                        serial_cur = 'Cam'
                        print("\nSwitched to Cam")

                # Exit manual mode
                if serial_port is not None:
                    scom.toggle_manual(serial_port)                
                
                # Speed
                if joystick.get_button(ctrl_map_btn['Select']):
                    scom.draw_highlight(highlight_surface, map_position['Select'])
                    cfg.speed_mode[serial_cur] = (cfg.speed_mode[serial_cur] + 1) % 3
                    scom.set_speed(serial_port, speed_array[cfg.speed_mode[serial_cur]])
                    print("Speed: " + str(speed_array[cfg.speed_mode[serial_cur]]))

                # Recalibrate
                if joystick.get_button(ctrl_map_btn['Square']):
                    scom.draw_highlight(highlight_surface, map_position['Square'])
                    calib_com = "HOME\r"
                    if serial_port is not None:
                        scom.send_command(serial_port, calib_com)
                        scom.receive_command(serial_port)
                        scom.receive_command(serial_port)

                        start_time = time.time()
                        while True:
                            recv_com = scom.receive_command(serial_port)
                            if "Homing complete" in recv_com:
                                print("Received :", recv_com)
                                break
                            if time.time() - start_time > 180:
                                print("Homing Timeout")
                                break
                        
                    else:
                        print("\nSent: " + calib_com)
                
                # Move to default position
                if joystick.get_button(ctrl_map_btn['Circle']):             
                    scom.draw_highlight(highlight_surface, map_position['Circle'])
                    next_pos = list(list(item) for item in default_pos)
                    scom.update_pos(serial_port, next_pos, 'ALL')
                    cur_est[serial_cur] = next_pos
                    if scom.move_to_pos(serial_port) != 1:
                        print("Return to Default Position Failed")

                # Get current position
                if joystick.get_button(ctrl_map_btn['X']):
                    scom.draw_highlight(highlight_surface, map_position['X']) 
                    print(cur_est[serial_cur])
                    cur_pos = scom.get_position(serial_port)
                    if cur_pos is not None:
                        cur_est[serial_cur] = cur_pos
                        print ('Current position:' + str(cur_pos))
                    else:
                        print("Failed to get position.")

                # Show Help Screen
                if joystick.get_button(ctrl_map_btn['Start']):
                    scom.draw_highlight(highlight_surface, map_position['Start'])
                    # Load image
                    help_image_path = 'Images/Help_screen.jpg'
                    help_image = pygame.image.load(help_image_path)
                    width, height = help_image.get_size()

                    help_screen = pygame.display.set_mode((width, height))
                    pygame.display.set_caption('Controller Help')
                    help_screen.blit(help_image, (0,0))
                    pygame.display.flip()

                    # Wait for Start button to be pressed again
                    while True:
                        event2 = pygame.event.wait()
                        if event2.type == pygame.QUIT:
                            return True, clr_flag, screen_text
                        elif event2.type == pygame.JOYBUTTONDOWN:
                            if joystick.get_button(ctrl_map_btn['Start']):
                                # Close help screen
                                width, height = image.get_size()
                                help_screen = pygame.display.set_mode((width*2, height))
                                pygame.display.set_caption('Controller Mapper')
                                help_screen.blit(help_image, (0,0))
                                pygame.display.flip()
                                break

                # Enter Manual Mode 
                if serial_port is not None:
                    scom.toggle_manual(serial_port)

            if event.type == pygame.JOYBUTTONUP: 
                clr_flag=True

            if event.type == pygame.QUIT:
                return True, clr_flag, screen_text
    return False, clr_flag, screen_text



def main():
    global serial_cam, serial_scalp, serial_cur, joint_mode

    # Initialize pygame and controller
    pygame.init()
    joystick = scom.controller_init()

    # Load image
    image_path = 'Images/PS4_ctrl_layout3.jpg'
    image = pygame.image.load(image_path)
    width, height = image.get_size()

    screen = pygame.display.set_mode((width*2, height))
    pygame.display.set_caption('Controller Mapper')

    cam_feed = cv2.VideoCapture(cam_usb)
    if not cam_feed.isOpened():
        print("Camera is not connected!")
        if not debug:
            exit(0)

    highlight_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    
    print('\n####### SCORBOT PROJECT #######\n')
    print('For controller help press Start')

    # Initialize Scalpel Robot
    serial_port = serial_scalp
    serial_cur = 'Scalpel'

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

        # Get current position Scalpel
        cur_est[serial_cur] = scom.get_position(serial_port)
        scom.set_speed(serial_port, speed_array[speed_mode[serial_cur]])

        # Display Response
        scom.send_command(serial_port, "ECHO\r")
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)

        scom.send_command(serial_port, "~\r")
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)

        # Control enable
        scom.send_command(serial_port, "c\r")
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)

        # Toggle XYZ mode
        scom.send_command(serial_port, "j\r")
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)
        joint_mode['Scalpel'] = 'JOINT'

    # Initialize Camera Robot
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

        # Get current position Cam
        cur_est[serial_cur] = scom.get_position(serial_port)
        scom.set_speed(serial_port, speed_array[speed_mode[serial_cur]])

        # Display Response
        scom.send_command(serial_port, "ECHO\r")
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)

        scom.send_command(serial_port, "~\r")
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)


        scom.send_command(serial_port, "j\r")
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)

        joint_mode['Cam'] = 'JOINT'

        scom.send_command(serial_port, "c\r")
        scom.receive_command(serial_port)
        scom.receive_command(serial_port)

    # Get controller input
    done = False
    while not done:
        screen.blit(image, (0,0))
        done, clr_screen, text = get_event(joystick, highlight_surface, image)
        ret, frame = cam_feed.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame = cv2.flip(frame, 0)
        frame = cv2.resize(frame, (height, width))
        pygame_frame = pygame.surfarray.make_surface(frame)
        
        # Update controller window
        if clr_screen:
            highlight_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        screen.blit(highlight_surface,(0,0))
        screen.blit(text[0],(30,30))
        screen.blit(text[1],(230,30))
        screen.blit(text[2],(450,30))
        screen.blit(pygame_frame, (width,0))
        help_text = pygame.font.SysFont("moonspace",30).render("Press Options For Help" ,1,(255,0,0))
        screen.blit(help_text, (190, 360))
        pygame.display.flip()
        

if __name__ == '__main__':
    main()