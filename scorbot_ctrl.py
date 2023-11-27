import pygame
import serial
import time



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
#PS3
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
                   'Anlg_R_vert': 3
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
ctrl_map_ps3_ax = {'Anlg_L_vert': 0,
                   'Anlg_L_horz': 1,
                   'Anlg_R_vert': 2,
                   'Anlg_R_vert': 3,
                   'Anlg_L2': 4,
                   'Anlg_R2': 5
                   }
speed = 10
default_pos = (0,0,0)
# Commands

speed_com = "SPEED " + str(speed)
default_com = "HERE " + str(default_pos)
teach_com = "TEACH "

# Send command to serial port
def send_command(port, command):
    
    port.write(command.encode())

    time.sleep(0.1)

def draw_highlight(highlight_surface, pos):
    highlight_color = (255, 255, 0) + (180,)
    highlight_radius = 25
    pygame.draw.circle(highlight_surface, highlight_color, pos, highlight_radius)

# Initialize serial port communication
def port_init(com_port):
    baud_rate = 9600
    try:
        ser = serial.Serial(com_port, baud_rate, timeout=1)
    except:
        print("Failed to connect to serial port.")
        return None
    return ser


# Initialize controller
def controller_init():
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No gamepad found.")
        return
    
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    return joystick


def main():

    # Initialize serial port communication
    com_port = 'COM7'
    ser = port_init(com_port)

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

    done = False
    while not done:
        for event in pygame.event.get():
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

            if event.type == pygame.JOYBUTTONDOWN:
                if joystick.get_button(ctrl_map_ps3_btn['Triangle']):
                    draw_highlight(highlight_surface, map_pos['Triangle'])
                if joystick.get_button(ctrl_map_ps3_btn['Square']):
                    draw_highlight(highlight_surface, map_pos['Square'])
                if joystick.get_button(ctrl_map_ps3_btn['Circle']):
                    draw_highlight(highlight_surface, map_pos['Circle'])
                if joystick.get_button(ctrl_map_ps3_btn['X']):
                    draw_highlight(highlight_surface, map_pos['X'])

                # if joystick.get_button(ctrl_map_ps3['Up']):
                #     draw_highlight(highlight_surface, map_pos['Up'])
                # if joystick.get_button(ctrl_map_ps3['Down']):
                #     draw_highlight(highlight_surface, map_pos['Down'])
                # if joystick.get_button(ctrl_map_ps3['Left']):
                #     draw_highlight(highlight_surface, map_pos['Left'])
                # if joystick.get_button(ctrl_map_ps3['Right']):
                #     draw_highlight(highlight_surface, map_pos['Right'])

                if joystick.get_button(ctrl_map_ps3_btn['L1']):
                    draw_highlight(highlight_surface, map_pos['L1'])
                if joystick.get_button(ctrl_map_ps3_btn['R1']):
                    draw_highlight(highlight_surface, map_pos['R1'])
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

        screen.blit(image, (0,0))
        screen.blit(highlight_surface,(0,0))
        pygame.display.flip()
        

if __name__ == '__main__':
    main()