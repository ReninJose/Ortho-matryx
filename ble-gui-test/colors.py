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

TITLE_COLOR = 'RGBWWRGWB'
MENU_COLOR = 'BXGBXGBXG'
AVATAR_COLOR = 'BBBBBBRXG'

ColorDict = {
    **dict.fromkeys(['X', 'x'], DEF),
    **dict.fromkeys(['W', 'w'], WHT),
    **dict.fromkeys(['R', 'r'], RED),
    **dict.fromkeys(['G', 'g'], GRN),
    **dict.fromkeys(['B', 'b'], BLU),
    **dict.fromkeys(['title'], TITLE_COLOR),
    **dict.fromkeys(['menu'], MENU_COLOR),
    **dict.fromkeys(['avatar'], AVATAR_COLOR)
}
