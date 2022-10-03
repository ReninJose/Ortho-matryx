# Authors: Ellis Hobbby, Ryan White
# Version: 2.0


"""---------------------------------------------
    
    Colors used for canvas itemconfig
    
    ColorDict is most important:
        > Enables color string to be
          converted to itemconfig color
          
    Other constants for easy utility reference

---------------------------------------------"""


DEF = 'gray25'
WHT = 'white'
RED = 'IndianRed1'
GRN = 'PaleGreen1'
BLU = 'SkyBlue1'

DEF_CONFIG = ('fill', 'default', DEF)
WHT_CONFIG = ('fill', 'white', WHT)
RED_CONFIG = ('fill', 'red', RED)
GRN_CONFIG = ('fill', 'green', GRN)
BLU_CONFIG = ('fill', 'blue', BLU)

DEF_PATTERN = 'XXXXXXXXX'
TITLE_COLOR = 'RGBWWRGWB'
MENU_COLOR = 'BXGBXGBXG'
AVATAR_COLOR = 'BBBBBBRXG'
WINNING_COLOR = 'XXXXWXXXX'
NAME_COLOR = 'WWWXXXRBG'


ColorDict = {
    **dict.fromkeys(['X', 'x'], DEF),
    **dict.fromkeys(['W', 'w'], WHT),
    **dict.fromkeys(['R', 'r'], RED),
    **dict.fromkeys(['G', 'g'], GRN),
    **dict.fromkeys(['B', 'b'], BLU),
    **dict.fromkeys(['title'], TITLE_COLOR),
    **dict.fromkeys(['menu'], MENU_COLOR),
    **dict.fromkeys(['avatar'], AVATAR_COLOR),
    **dict.fromkeys(['winning'], WINNING_COLOR),
    **dict.fromkeys(['name'], NAME_COLOR),
    **dict.fromkeys(['default color'], DEF),
    **dict.fromkeys(['default pattern'], DEF_PATTERN)
}
