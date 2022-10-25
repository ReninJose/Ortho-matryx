# Authors: Ellis Hobbby, Ryan White
# Version: 2.0


"""---------------------------------------------
    
    Tags used for canvas itemconfig control  

---------------------------------------------"""


MATRIX_SIZE = 9

title_img = [None] * 9

title_txt = [None] * 9
title_txt[3] = 'title ortho'
title_txt[4] = 'title matryx'
title_txt[7] = 'title game'

#############################

menu_img = [None] * 9

menu_txt = [None] * 9
menu_txt[0] = 'menu play'
menu_txt[2] = 'menu avatar'
menu_txt[6] = 'menu quit'
menu_txt[8] = 'menu score'

#############################

avatar_img = [None] * 9
avatar_img[0] = 'avatar 0'
avatar_img[1] = 'avatar 1'
avatar_img[2] = 'avatar 2'
avatar_img[3] = 'avatar 3'
avatar_img[4] = 'avatar 4'
avatar_img[5] = 'avatar 5'

avatar_txt = [None] * 9
avatar_txt[6] = 'avatar back'
avatar_txt[8] = 'avatar play'

#############################

winning_img = [None] * 9
winning_txt = [None] * 9
winning_txt[0] = 'winning show'
winning_txt[1] = 'winning win'
winning_txt[2] = 'winning color'
winning_txt[4] = 'winning count'

#############################

name_img = [None] * 9

name_txt = [None] * 9
name_txt[0] = 'name 0'
name_txt[1] = 'name 1'
name_txt[2] = 'name 2'
name_txt[6] = 'name minus'
name_txt[7] = 'name enter'
name_txt[8] = 'name plus'

#############################

start_txt = [None] * 9
start_txt[4] = 'start game'

#############################

post_txt = [None] * 9
post_txt[0] = 'post round'
post_txt[1] = 'post score'
post_txt[4] = 'post session'
post_txt[5] = 'post total'
post_txt[6] = 'post menu'
post_txt[7] = 'post high'
post_txt[8] = 'post play'

#############################



background = ('clear background', 'matrix background', 'highscore background')
background_txt = ('clear text','matrix text', 'highscore scores')
background_img = None

#############################

button = []
button_txt = []
button_img = []

for i in range(MATRIX_SIZE):
    button.append(('clear button', 'matrix button'))
    button_txt.append(('clear text', 'matrix text', 
                        title_txt[i], menu_txt[i], 
                        avatar_txt[i], name_txt[i],
                        start_txt[i], winning_txt[i],
                        post_txt[i]
                        ))
    button_img.append(('clear image', avatar_img[i]))

#############################

Tags = {
    'button': button,
    'button text': button_txt,
    'button image': button_img,
    'background': background,
    'background text': background_txt,
    'background image': background_img
    }
