'''
Authors: 
    Diogo Rosa   - 93044
    Tomás Bastos - 93194
    Tiago Simões - 96329
'''

map_position = { 'X': (552,234), 
                 'Circle': (600,188), 
                 'Square': (506,188), 
                 'Triangle': (552,142), 
                 'Share': (236,128),
                 'Select': (236,128),
                 'PS': (362,274), 
                 'Options': (487,127),
                 'Start': (487,127), 
                 'L3': (264,272), 
                 'R3': (460,272), 
                 'L1': (176,86),
                 'R1': (543,86),
                 'Up': (172, 158), 
                 'Down': (172,217), 
                 'Left': (142,188),
                 'Right': (200,188),
                 'Touchpad': (360,153)
                 }


# PS4 Controller Mapping
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