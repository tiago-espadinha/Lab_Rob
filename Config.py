'''
Authors: 
    Diogo Rosa   - 93044
    Tomás Bastos - 93194
    Tiago Simões - 96329
'''

debug = True

pos_var = 'A31'
controller = 'PS4'

# Serial ports
scalp_port = 'COM7'
cam_port   = 'COM3'

# Movement speed
speed_array = [5, 15, 30]
speed_mode = {'Cam': 1, 'Scalp':1}

# Analog stick deadzone
deadzone = 0.5

# [Base, Shoulder, Elbow, Wrist Pitch, Wrist Roll]
limits_joint = [[20000, -20000],[-6500, 12000],[-26000, 3900],[-25000, 25000],[-31000, 31000]]
# [X, Y, Z, P, R]
limits_xyz = [[2000, 5500],[-2300, 2300],[-1300, 9400],[-1400, 240],[2700, 2700]]

# Default position [[Base, Shoulder, Elbow, Wrist Pitch, Wrist Roll][X, Y, Z, P, R]]
default_pos = ((1300, -11700, -5480, -10300, 2140),(5000, 100, 8000, 0, 0))
default_pos_cam1 = ((-860, -14850, -430, -27000, -2930),(3100, -540, 7900, -200, -480)) # Camera position to see robot
default_pos_cam2 = ((-300, -15720, -28440, -4050, -2720),(2980, -410, 2810, -540, -460)) # Camera position to see gelatin




# [[  -80  6389 -9621 -9133 >31928]   [ 5121  -381   185  -833  >2792]] - limit eixo 5 roll esquerda
# [[   -80   6389  -9621  -9133 >-31946] [  5121   -381    185   -833   >2948]] - limit eixo 5 roll direita

# [[   -84   5348 -12897  >28123 -31946]  [  6708   -391   3704    >244   2948]] - limit eixo 4 pitch cima
# [[   -96   4524 -13648 >-26928 -31946] [  2246   -368   1465  >-1473   2948]]  - limit eixo 4 pitch baixo

# [[>-21593    241 -13494 -23634 -31271] [  > -37  -3212   1803  -1197   3011]] - limit eixo 1 base direita
# [[ >20475  -1739 -13493 -23634 -31270] [   >941   3295   2182  -1120   3011]] - limit eixo 1 base esquerda

# [[   848  -7171   >3970 -22218 -31947] [  5210    -52   >7703   -181   2948]] - limit eixo 3 elbow cima
# [[   848  -7474 >-26887   3593 -31946] [  3690   -140   >2107   -568   2948]] - limit eixo 3 elbow baixo

# [[   829  >10985   2365  -8783 -31945] [  7297     >59    733   -533   2948]] - limit eixo 2 shoulder baixo
# [[   827  >-6737  11357 -17811 -31946] [  4140   >-120   9885    228   2948]] - limit eixo 2 shoulder cima

# [[  -696 -10234 -28433   7174   1303] [  3807   -534   2751   -409    -79]] default camera

# [[   481   9987   8491 -12463   3688] [  7985    -91   2625   -370    144]] esticadinho para a frente
# [[  9719   9994   8531 -12073   3687] [  6534   4650   2676   -356    144]] esticadinho esquerda
# [[ -6792   9988   8531 -12073   3687] [  7011  -3895   2680   -356    144]] esticadinho direita

# [[  9358  18725   8531 -12073   3687] [  5199   3415  -1379   -698    144]] esticadinho baixo
# [[  1734  -4745   8531 -12073   3687] [  5300    274   9439    219    144]] esticadinho cima

# [[ -6650   8960 -19466    713   3686] [  2089  -1410   -766  -1010    144]] limite x-
# [[ -2132  12612    283 -12614   3686] [  5798  -1206   -600   -798    144]] limite x+

# [[ -5147  11962  -1403 -11322   3682] [  5328  -2326   -602   -798    144]] limite y+
# [[  7567  12343   -197 -12238   3680] [  5313   2607   -570   -794    144]] limite y-


#         inicio > final >> delta
# deltaBase 2219 > 2996 >> 66  -  11.77
# delta   > 2977 >> 105       9.8
# deltaBase  5.6

# deltaShoulder 19
# deltaShoulder buja 5.8
# deltaShoulder baixo 8.6
# deltaShoulder buja cima