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

print(CWD)

if CWD[-3:] != 'app':
    print('adding gui-app')
    CWD = os.path.join(CWD, 'gui-app')
    

AVATAR_PATH = os.path.join(CWD, 'images/')
SOUNDS = os.path.join(CWD, 'sounds/')

print(SOUNDS)


MAIN_DIR = CWD[:CWD.rfind('gui')]
BACKEND_DIR = os.path.join(MAIN_DIR, 'backend')

print(MAIN_DIR)
print(BACKEND_DIR)


BACKEND_PATH = os.path.join(BACKEND_DIR, 'backend')
BACKEND_ARG_COLOR = 'cg'
BACKEND_ARG_SCOREBOARD = 'sb'

CORRECT_COLOR = os.path.join(BACKEND_DIR, 'color_rand_gen', 'correct_color.txt')
COLOR_PATTERN = os.path.join(BACKEND_DIR, 'color_rand_gen', 'color_pattern.txt')

SCOREBOARD = os.path.join(BACKEND_DIR, 'score_board', 'sb.txt')


