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

DEFAULT = 'XXXXXXXXX'

ColorDict = {
    **dict.fromkeys(['X', 'x'], DEF),
    **dict.fromkeys(['W', 'w'], WHT),
    **dict.fromkeys(['R', 'r'], RED),
    **dict.fromkeys(['G', 'g'], GRN),
    **dict.fromkeys(['B', 'b'], BLU),
}
