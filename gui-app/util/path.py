# Authors: Ellis Hobbby, Ryan White
# Version: 2.0
import os


"""---------------------------------------------
    
    Paths used by main program files
    
        > app.py
        > gui.py
        > menus.py
        > game.py

---------------------------------------------"""


CWD = os.getcwd()

if CWD[-3:] != 'app':
    print('adding gui-app')
    CWD = os.path.join(CWD, 'gui-app')
    

AVATAR_PATH = os.path.join(CWD, 'images/')
SOUNDS = os.path.join(CWD, 'sounds/')

B1_WAV = SOUNDS + 'B1.wav'
B2_WAV = SOUNDS + 'B2.wav'
B3_WAV = SOUNDS + 'B3.wav'
B4_WAV = SOUNDS + 'B4.wav'
B5_WAV = SOUNDS + 'B5.wav'
B6_WAV = SOUNDS + 'B6.wav'
B7_WAV = SOUNDS + 'B7.wav'
B8_WAV = SOUNDS + 'B8.wav'
B9_WAV = SOUNDS + 'B9.wav'
THEME_WAV = SOUNDS + 'Theme.wav'


MAIN_DIR = CWD[:CWD.rfind('gui')]
BACKEND_DIR = os.path.join(MAIN_DIR, 'backend')


BACKEND_PATH = os.path.join(BACKEND_DIR, 'backend')
BACKEND_ARG_COLOR = 'cg'
BACKEND_ARG_SCOREBOARD = 'sb'

CORRECT_COLOR = os.path.join(BACKEND_DIR, 'color_rand_gen', 'correct_color.txt')
COLOR_PATTERN = os.path.join(BACKEND_DIR, 'color_rand_gen', 'color_pattern.txt')

SCOREBOARD = os.path.join(BACKEND_DIR, 'score_board', 'sb.txt')


