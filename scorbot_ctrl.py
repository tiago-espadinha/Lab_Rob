import pygame
import serial
import time

#daddy

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

ctrl_map_ps4 = {'X': 0, 
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
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (128,), (492,170), 25)
                if event.key == ctrl_map_key['Square']:
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (447,215), 25)
                if event.key == ctrl_map_key['Circle']:
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (537,215), 25)
                if event.key == ctrl_map_key['X']:
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (492,260), 25)

                if event.key == ctrl_map_key['Up']:
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (160,185), 25)
                if event.key == ctrl_map_key['Down']:
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (160,245), 25)
                if event.key == ctrl_map_key['Left']:
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (130,215), 25)
                if event.key == ctrl_map_key['Right']:
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (190,215), 25)

                if event.key == ctrl_map_key['L1']:
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (160,90), 25)
                if event.key == ctrl_map_key['R1']:
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (492,90), 25)
                if event.key == ctrl_map_key['L3']:
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (242,298), 25)
                if event.key == ctrl_map_key['R3']:
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (410,298), 25)

                if event.key == ctrl_map_key['Options']:
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (375,215), 25)
                if event.key == ctrl_map_key['Share']:
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (275,215), 25)
                if event.key == ctrl_map_key['PS']:
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (326,249), 25)
                if event.key == ctrl_map_key['Touchpad']:
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (326,175), 25)

            if event.type == pygame.JOYBUTTONDOWN:
                if joystick.get_button(ctrl_map_ps4['Triangle']):
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (128,), (492,170), 25)
                if joystick.get_button(ctrl_map_ps4['Square']):
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (447,215), 25)
                if joystick.get_button(ctrl_map_ps4['Circle']):
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (537,215), 25)
                if joystick.get_button(ctrl_map_ps4['X']):
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (492,260), 25)

                if joystick.get_button(ctrl_map_ps4['Up']):
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (160,185), 25)
                if joystick.get_button(ctrl_map_ps4['Down']):
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (160,245), 25)
                if joystick.get_button(ctrl_map_ps4['Left']):
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (130,215), 25)
                if joystick.get_button(ctrl_map_ps4['Right']):
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (190,215), 25)

                if joystick.get_button(ctrl_map_ps4['L1']):
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (160,90), 25)
                if joystick.get_button(ctrl_map_ps4['R1']):
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (492,90), 25)
                if joystick.get_button(ctrl_map_ps4['L3']):
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (242,298), 25)
                if joystick.get_button(ctrl_map_ps4['R3']):
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (410,298), 25)

                if joystick.get_button(ctrl_map_ps4['Options']):
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (375,215), 25)
                if joystick.get_button(ctrl_map_ps4['Share']):
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (275,215), 25)
                if joystick.get_button(ctrl_map_ps4['PS']):
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (326,249), 25)
                if joystick.get_button(ctrl_map_ps4['Touchpad']):
                    pygame.draw.circle(highlight_surface, (255, 255, 0) + (180,), (326,175), 25)
            
            if event.type == pygame.KEYUP or event.type == pygame.JOYBUTTONUP:
                highlight_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)

            if event.type == pygame.QUIT:
                done = True
        screen.blit(image, (0,0))
        screen.blit(highlight_surface,(0,0))
        pygame.display.flip()
        

if __name__ == '__main__':
    main()