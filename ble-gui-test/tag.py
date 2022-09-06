MATRIX_SIZE = 9

title_img = [None] * 9

title_txt = [None] * 9
title_txt[3] = 'title ortho'
title_txt[4] = 'title matryx'
title_txt[7] = 'title game'


menu_img = [None] * 9

menu_txt = [None] * 9
menu_txt[0] = 'menu avatar'
menu_txt[2] = 'menu play'


avatar_img = [None] * 9

avatar_txt = [None] * 9
avatar_txt[6] = 'avatar back'
avatar_txt[8] = 'avatar play'


button = []
button_txt = []
button_img = []

background = ('clear background', 'matrix background', 'highscore background')
background_txt = ('clear text','matrix text', 'highscore scores')
background_img = None

for i in range(MATRIX_SIZE):
    button.append(('clear button', 'matrix button'))
    button_txt.append(('clear text', 'matrix text', title_txt[i], menu_txt[i], avatar_txt[i]))
    button_img.append(None)



Tags = {
    'button': button,
    'button text': button_txt,
    'button image': button_img,
    'background': background,
    'background text': background_txt,
    'background image': background_img
    }
