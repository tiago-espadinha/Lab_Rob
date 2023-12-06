import pygame
import serial
import time
import numpy as np

import ScorbotCom as scom
import ScorbotCtrl as sctrl
import CtrlMapping as ctrlmap

controller = "PS4"

map_position = { 'X': (492,260), 
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

# Lab Controller Mapping 
if controller == "PS3":
    # Buttons
    ctrl_map_btn = {'X': 0, 
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
    ctrl_map_ax = {'Anlg_L_vert': 0,
                   'Anlg_L_horz': 1,
                   'Anlg_R_vert': 2,
                   'Anlg_R_horz': 3
                   }


# PS4 Controller Mapping
elif controller == "PS4":
    # Buttons
    ctrl_map_btn = {'X': 0, 
                    'Circle': 1, 
                    'Square': 2, 
                    'Triangle': 3, 

                    'Select': 4, 
                    'PS': 5, 
                    'Start': 6, 

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
    ctrl_map_ax = {'Anlg_L_horz': 0,
                   'Anlg_L_vert': 1,
                   'Anlg_R_horz': 2,
                   'Anlg_R_vert': 3,
                   'Anlg_L2': 4,
                   'Anlg_R2': 5
                   }