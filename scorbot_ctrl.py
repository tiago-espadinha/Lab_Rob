import pygame
import serial
import time
import numpy as np


map_pos = { 'X': (492,260), 
            'Circle': (537,215), 
            'Square': (447,215), 
            'Triangle': (492,170), 
            'Share': (275,215),
            'Select': (275,215),
            'PS': (326,249), 
            'Options': (375,215),
            'Start': (375,215), 
            'L3': (242,298), 
            'R3': (410,298), 
            'L1': (160,90),
            'R1': (492,90),
            'Up': (160,185), 
            'Down': (160,245), 
            'Left': (130,215),
            'Right': (190,215),
            'Touchpad': (326,175)
            }

ctrl_map_key = {'X': pygame.K_k, 
                'Circle': pygame.K_l, 
                'Square': pygame.K_j, 
                'Triangle': pygame.K_i, 
                'Share': pygame.K_n, 
                'PS': pygame.K_SPACE, 
                'Options': pygame.K_m, 
                'L3': pygame.K_z, 
                'R3': pygame.K_x, 
                'L1': pygame.K_q,
                'R1': pygame.K_e,
                'Up': pygame.K_w, 
                'Down': pygame.K_s, 
                'Left': pygame.K_a,
                'Right': pygame.K_d,
                'Touchpad': pygame.K_c
                }

# PS3
# Buttons
ctrl_map_ps5_btn = {'X': 0, 
                    'Square': 1, 
                    'Circle': 2, 
                    'Triangle': 3, 

                    'L1': 4,
                    'L2': 5,
                    'R1': 6,
                    'R2': 7,

                    'Select': 8,
                    'Start': 9,
                    'L3': 10, 
                    'R3': 11, 
                    }

# Axes
'''
Analog Left
    Axis 0: 
        left = -1 
        right = 1
    Axis 1: 
        up = -1
        down = 1

Analog Right
    Axis 2: 
        left = -1 
        right = 1
    Axis 3: 
        up = -1 
        down = 1
'''
ctrl_map_ps5_ax = {'Anlg_L_vert': 0,
                   'Anlg_L_horz': 1,
                   'Anlg_R_vert': 2,
                   'Anlg_R_horz': 3
                   }

#PS4
ctrl_map_ps3_btn = {'X': 0, 
                'Circle': 1, 
                'Square': 2, 
                'Triangle': 3, 

                'Share': 4, 
                'PS': 5, 
                'Options': 6, 

                'L3': 7, 
                'R3': 8, 
                'L1': 9,
                'R1': 10,

                'Up': 11, 
                'Down': 12, 
                'Left': 13,
                'Right': 14,

                'Touchpad': 15
                }
ctrl_map_ps3_ax = {'Anlg_L_vert': 1,
                   'Anlg_L_horz': 0,
                   'Anlg_R_vert': 3,
                   'Anlg_R_horz': 2,
                   'Anlg_L2': 4,
                   'Anlg_R2': 5
                   }

speed = 10
# Default position [X, Y, Z, P, R]
default_pos = [5000, 100, 8000, 0, 0]
# Commands

speed_com = "SPEED " + str(speed)
default_com = "HERE " + str(default_pos)
teach_com = "TEACH "
list_com = "LISTPV A31\r"
del_com = "DELP A31"
here_com = "HERE A32\r"


# Send commands to move robot
def move_to_pos(serial_port, pos, move_type):
    if move_type == 'up' or move_type == 'down':
        set_pos_com = "SETPVC A31 X " + str(pos[0]) + "\r"
    if move_type == 'left' or move_type == 'right':
        set_pos_com = "SETPVC A31 Y " + str(pos[1]) + "\r"
    if move_type == 'forward' or move_type == 'backward':
        set_pos_com = "SETPVC A31 Z " + str(pos[2]) + "\r"
    send_command(serial_port, set_pos_com)
    receive_command(serial_port)
    recv_com=receive_command(serial_port)
    send_command(serial_port, "MOVE A31 100\r")
    receive_command(serial_port)
    recv_com=receive_command(serial_port)
    return 1


# Send command to get current position
def get_pos(serial_port):
    # Save current position
    pos_com = "HERE A31\r"
    send_command(serial_port, pos_com)
    receive_command(serial_port)
    recv_com=receive_command(serial_port)

    # Get current coordinates
    if 'Done' in recv_com:
        pos_com = "LISTPV A31\r"
        send_command(serial_port, pos_com)
        receive_command(serial_port)
        recv_com=receive_command(serial_port)

        if 'Position' in recv_com:
            receive_command(serial_port)
            recv_com=receive_command(serial_port)
            split_com = split(recv_com, "   ")
            new_split_com = np.zeros(5, dtype=int)

            # Split string and save coordinates
            for i in range(5):
                aux = split(split_com[i], ":")
                new_split_com[i] = int(aux[1])
            return new_split_com
    return 0


# Split message string
def split(string, split_char):
    str_array = string.split(split_char)
    return str_array


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
    print("Sent: ", command.encode('utf8'))
    port.write(command.encode('utf8'))
    time.sleep(0.1)
    
    
# Receive command from serial port
def receive_command(port):
    message = port.readline()
    message = message.decode('utf8')
    print("Recived: ", message)
    return message


def main():

    # Initialize serial port communication
    port_name = 'COM7'
    serial_port = port_init(port_name)

    # Initialize pygame and controller
    pygame.init()
    joystick = controller_init()


    ### Button Layout ###
    # Load image
    image_path = 'Images/PS3_ctrl_layout.jpg'
    image = pygame.image.load(image_path)
    width, height = image.get_size()

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Controller Mapper')

    highlight_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)

    # Get controller input
    done = False
    while not done:
        for event in pygame.event.get():
            # Keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == ctrl_map_key['Triangle']:
                    draw_highlight(highlight_surface, map_pos['Triangle'])
                if event.key == ctrl_map_key['Square']:
                    draw_highlight(highlight_surface, map_pos['Square'])
                if event.key == ctrl_map_key['Circle']:
                    draw_highlight(highlight_surface, map_pos['Circle'])
                if event.key == ctrl_map_key['X']:
                    draw_highlight(highlight_surface, map_pos['X'])

                if event.key == ctrl_map_key['Up']:
                    draw_highlight(highlight_surface, map_pos['Up'])
                if event.key == ctrl_map_key['Down']:
                    draw_highlight(highlight_surface, map_pos['Down'])
                if event.key == ctrl_map_key['Left']:
                    draw_highlight(highlight_surface, map_pos['Left'])
                if event.key == ctrl_map_key['Right']:
                    draw_highlight(highlight_surface, map_pos['Right'])
                    

                if event.key == ctrl_map_key['L1']:
                    draw_highlight(highlight_surface, map_pos['L1'])
                if event.key == ctrl_map_key['R1']:
                    draw_highlight(highlight_surface, map_pos['R1'])
                if event.key == ctrl_map_key['L3']:
                    draw_highlight(highlight_surface, map_pos['L3'])
                if event.key == ctrl_map_key['R3']:
                    draw_highlight(highlight_surface, map_pos['R3'])

                if event.key == ctrl_map_key['Options']:
                    draw_highlight(highlight_surface, map_pos['Options'])
                if event.key == ctrl_map_key['Share']:
                    draw_highlight(highlight_surface, map_pos['Share'])
                if event.key == ctrl_map_key['PS']:
                    draw_highlight(highlight_surface, map_pos['PS'])
                if event.key == ctrl_map_key['Touchpad']:
                    draw_highlight(highlight_surface, map_pos['Touchpad'])
            
            # Controller input
            if event.type == pygame.JOYAXISMOTION:
                if joystick.get_axis(ctrl_map_ps3_ax['Anlg_L_vert']) < -0.5:
                    draw_highlight(highlight_surface, map_pos['Up'])
                    next_pos = cur_pos
                    next_pos[0] += 100
                    if move_to_pos(serial_port, next_pos, 'up') == 1:
                        cur_pos = next_pos
                if joystick.get_axis(ctrl_map_ps3_ax['Anlg_L_vert']) > 0.5:
                    draw_highlight(highlight_surface, map_pos['Down'])
                    next_pos = cur_pos
                    next_pos[0] -= 100
                    if move_to_pos(serial_port, next_pos, 'down') == 1:
                        cur_pos = next_pos
                if joystick.get_axis(ctrl_map_ps3_ax['Anlg_L_horz']) < -0.5:
                    draw_highlight(highlight_surface, map_pos['Left'])
                    next_pos = cur_pos
                    next_pos[1] += 100
                    if move_to_pos(serial_port, next_pos, 'left') == 1:
                        cur_pos = next_pos
                if joystick.get_axis(ctrl_map_ps3_ax['Anlg_L_horz']) > 0.5:
                    draw_highlight(highlight_surface, map_pos['Right'])
                    next_pos = cur_pos
                    next_pos[1] -= 100
                    if move_to_pos(serial_port, next_pos, 'right') == 1:
                        cur_pos = next_pos
                if joystick.get_axis(ctrl_map_ps3_ax['Anlg_R_vert']) < -0.5:
                    draw_highlight(highlight_surface, map_pos['Triangle'])
                if joystick.get_axis(ctrl_map_ps3_ax['Anlg_R_vert']) > 0.5:
                    draw_highlight(highlight_surface, map_pos['X'])
                if joystick.get_axis(ctrl_map_ps3_ax['Anlg_R_horz']) < -0.5:
                    draw_highlight(highlight_surface, map_pos['Square'])
                if joystick.get_axis(ctrl_map_ps3_ax['Anlg_R_horz']) > 0.5:
                    draw_highlight(highlight_surface, map_pos['Circle'])

            if event.type == pygame.JOYBUTTONDOWN:
                if joystick.get_button(ctrl_map_ps3_btn['Triangle']):
                    if serial_port != None:
                        send_command(serial_port, here_com)
                        receive_command(serial_port)
                        receive_command(serial_port)
                        receive_command(serial_port)
                        receive_command(serial_port)
                    draw_highlight(highlight_surface, map_pos['Triangle'])
                if joystick.get_button(ctrl_map_ps3_btn['Square']):
                    draw_highlight(highlight_surface, map_pos['Square'])
                    if serial_port != None:   
                        cur_pos = get_pos(serial_port)
                        print ('Current position:' + str(cur_pos))
                if joystick.get_button(ctrl_map_ps3_btn['Circle']):
                    if serial_port != None:    
                        print(del_com)
                        send_command(serial_port, del_com)               
                    draw_highlight(highlight_surface, map_pos['Circle'])
                if joystick.get_button(ctrl_map_ps3_btn['X']):
                    if serial_port != None:
                        send_command(serial_port, list_com)
            
                        info = receive_command(serial_port)
                        receive_command(serial_port)
                        receive_command(serial_port)
                        receive_command(serial_port)
                        receive_command(serial_port)
                        info_array = split(info, " ")
                        final_array = np.zeros(len(info_array))
                        print("INFO: ", info_array)
                        for i in range(len(info_array)):
                            aux = split(info_array[i], ":")
                            final_array[i] = aux[1]
                        print(final_array)
                    draw_highlight(highlight_surface, map_pos['X'])

                if joystick.get_button(ctrl_map_ps3_btn['Up']):
                    draw_highlight(highlight_surface, map_pos['Up'])
                    next_pos = cur_pos
                    next_pos[0] += 100
                    if move_to_pos(serial_port, next_pos, 'up') == 1:
                        cur_pos = next_pos
                if joystick.get_button(ctrl_map_ps3_btn['Down']):
                    draw_highlight(highlight_surface, map_pos['Down'])
                    next_pos = cur_pos
                    next_pos[0] -= 100
                    if move_to_pos(serial_port, next_pos, 'down') == 1:
                        cur_pos = next_pos
                if joystick.get_button(ctrl_map_ps3_btn['Left']):
                    draw_highlight(highlight_surface, map_pos['Left'])
                    next_pos = cur_pos
                    next_pos[1] += 100
                    if move_to_pos(serial_port, next_pos, 'left') == 1:
                        cur_pos = next_pos
                if joystick.get_button(ctrl_map_ps3_btn['Right']):
                    draw_highlight(highlight_surface, map_pos['Right'])
                    next_pos = cur_pos
                    next_pos[1] -= 100
                    if move_to_pos(serial_port, next_pos, 'right') == 1:
                        cur_pos = next_pos

                if joystick.get_button(ctrl_map_ps3_btn['L1']):
                    draw_highlight(highlight_surface, map_pos['L1'])
                    next_pos = cur_pos
                    next_pos[2] -= 100
                    if move_to_pos(serial_port, next_pos, 'forward') == 1:
                        cur_pos = next_pos
                if joystick.get_button(ctrl_map_ps3_btn['R1']):
                    draw_highlight(highlight_surface, map_pos['R1'])
                    next_pos = cur_pos
                    next_pos[2] += 100
                    if move_to_pos(serial_port, next_pos, 'backward') == 1:
                        cur_pos = next_pos
                if joystick.get_button(ctrl_map_ps3_btn['L3']):
                    draw_highlight(highlight_surface, map_pos['L3'])
                if joystick.get_button(ctrl_map_ps3_btn['R3']):
                    draw_highlight(highlight_surface, map_pos['R3'])

                # if joystick.get_button(ctrl_map_ps3['Options']):
                #     draw_highlight(highlight_surface, map_pos['Options'])
                # if joystick.get_button(ctrl_map_ps3['Share']):
                #     draw_highlight(highlight_surface, map_pos['Share'])
                # if joystick.get_button(ctrl_map_ps3['PS']):
                #     draw_highlight(highlight_surface, map_pos['PS'])
                # if joystick.get_button(ctrl_map_ps3['Touchpad']):
                #     draw_highlight(highlight_surface, map_pos['Touchpad'])
            
            if event.type == pygame.KEYUP or event.type == pygame.JOYBUTTONUP:
                highlight_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)

            if event.type == pygame.QUIT:
                done = True

        # Update controller window
        screen.blit(image, (0,0))
        screen.blit(highlight_surface,(0,0))
        pygame.display.flip()
        

if __name__ == '__main__':
    main()