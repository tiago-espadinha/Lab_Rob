'''
Authors: 
    Diogo Rosa   - 93044
    Tomás Bastos - 93194
    Tiago Simões - 96329
'''

debug = True

# Serial ports
scalp_port = 'COM7'
cam_port   = 'COM8'

pos_var = 'A31'

# Movement speed
speed_array = [5, 15, 30]
speed_mode = {'Cam': 1, 'Scalp':1}

# Analog stick deadzone
deadzone = 0.5

# [Base, Shoulder, Elbow, Wrist Pitch, Wrist Roll]
limits_joint = [[20000, -20000],[-6500, 12000],[-26000, 3900],[-25000, 25000],[-31000, 31000]]
# [X, Y, Z, P, R]
limits_xyz = [[2000, 5500],[-2300, 2300],[-1300, 9400],[-1400, 240],[-2700, 2700]]

# Default position [[Base, Shoulder, Elbow, Wrist Pitch, Wrist Roll][X, Y, Z, P, R]]
default_pos = ((984, -15720, -28440, 13737, 1367),(4058, -81, 4905, 10, -73))

# Delta 
# [Base, Shoulder, Elbow, Wrist Pitch]][X, Y, Z, P]
delta = [[[3, 1.8, 2.3, 4.2],[0, 0, 0, 0]], # Speed 5
         [[5, 3, 3.8, 7],[0, 0, 0, 0]], # Speed 15
         [[8, 4.8, 5, 11.2],[0, 0, 0, 0]]] # Speed 30