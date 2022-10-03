# Authors: Ellis Hobbby, Ryan White
# Version: 2.0


import tkinter as tk
import asyncio
from util import color, config, tag, path
from PIL import Image, ImageTk


"""---------------------------------------------
    
    IMPORTANT INFO:

    * Must change paths in /util/path.py *
    

---------------------------------------------"""


# constants for matrix dimensions
COL = 3; ROW = 3
MATRIX_SIZE = 9

        
class GUI(tk.Canvas):
    '''
    Main GUI view
    
    > Creates canvas items based off parent frame screen size
    
        > Background items:
            centered square, text, image. Based off screen height
            
        > Button items:
            3x3 matrix of circles. Text and image centered on both
            
        > Side panels:
            Left, right panels. Text and image split to top, mid, bot positions
    
    > Items controlled using item tags sent as dictionaries (see tag.py / config.py)
    
    > Asychronous updates every 1/120 seconds
    
    :param parent: tkinter frame obj sent from controller
    
    :param interval: time in seconds for screen updates
    '''
    
    def __init__(self, parent, font, interval=1/120):
        
        height = parent.winfo_height()
        width = parent.winfo_width()
        
        # create inherited canvas using screen dimensions of parent frame
        super().__init__(parent, width=width, height=height, bg = 'black', highlightthickness=0)
        self.pack()
        
        self.interval = interval
        self.font = font
        print('Font in GUI: ')
        print(self.font)
        
        
        clear_settings = [
            ('button', {'fill': None}),
            ('background', {'fill': None}), 
            ('text', {'text': None, 'fill': 'black', 
                      'font': self.font, 'justify': 'center'}), 
            ('image', {'image': None})  
        ]
        
        self.clear_config = config.GenericConfig('clear', 'hidden', clear_settings).configs
    
        
        # list reference background items
        self.background=[]  
        self.background_txt=[]  
        self.background_img=[]
        
        
        # list reference for button images
        self.button_avatars=[]
        
        # list reference button items
        self.button=[] 
        self.button_txt=[] 
        self.button_img=[]
        
        
        # list reference for panel images
        self.panel_avatars=[]
        
        # var reference left panel items
        self.left_rec=None
        
        self.left_mid_txt=None
        self.left_top_txt=None
        self.left_bot_txt=None
        
        self.left_mid_img=None
        self.left_top_img=None
        self.left_bot_img=None
        
        # var reference right panel items
        self.right_rec=None
        
        self.right_mid_txt=None
        self.right_top_txt=None
        self.right_bot_txt=None
        
        self.right_mid_img=None
        self.right_top_img=None
        self.right_bot_img=None
        

        # initate all canvas items
        self.upload_avatars(width, height)
        self.create_background_items(width, height)
        self.create_button_items(width, height)
        self.create_side_panels(width, height)
        
        
    def upload_avatars(self, width, height):
        '''

        Upload avatar images and resize accordingly.
        Added to avatar lists for reference.
        
        :param width: parent frame width
        :param height: parent frame height
        
        '''
        
        # image size for buttons
        b_size = int(height / 6)
        
        # image size for panels
        p_size = int((width-height) / 2.5)
        
        
        # upload and create panel / button images
        for i in range(6):
            b_img = (Image.open(path.AVATAR_PATH + str(i) + '.png').resize((b_size,b_size)).convert('RGBA'))
            p_img = (Image.open(path.AVATAR_PATH + str(i) + '.png').resize((p_size,p_size)).convert('RGBA'))
            self.button_avatars.append(ImageTk.PhotoImage(b_img))
            self.panel_avatars.append(ImageTk.PhotoImage(p_img))


        # fill extra list space button_avatars
        # will run into problems if it does
        # not equal matrix size (9)
        for i in range(3):
            self.button_avatars.append(None)
            
            
    def create_background_items(self, width, height):
        '''

        Create canvas background items.
        Will be based of square centered on screen.
        Square sides will be same as parent frame height
        
        :param width: parent frame width
        :param height: parent frame height
        
        '''
        
        # helps create square background
        # based off screen height
        offset = (width-height) / 2
        
        # plot vals for background rect
        x1 = y1 = offset
        x2 = height + offset
        y2 = height
        
        # plot vals for background text, image
        x3 = width / 2
        y3 = height / 2
        
        # create tuples for plot vals
        bounds = (x1, y1, x2, y2)
        center = (x3, y3)
        
        
        # creating background items
        self.background.append(
            self.create_rectangle( 
                bounds,
                tags=tag.background 
            )
        )
        self.background_txt.append(
            self.create_text( 
                center, fill='black', 
                font=self.font, justify='left', 
                tags=tag.background_txt
            )
        )
        self.background_img.append(
            self.create_image(
                center,
                tags=tag.background_img 
            )
        )
        
    def create_button_items(self, width, height):
        '''

        Create canvas button items.
        3x3 matrix of perfect circles.
        Based off square centered on screen.
        text and images centered on circles
        
        :param width: parent frame width
        :param height: parent frame height
        
        '''
        
        # helps center items in square 
        # background based off screen height
        offset = (width-height) /2
        
        # val for matrix cell dimension
        cell = (height / 3)
        
        # middle point of each cell
        midd = cell / 2
        
        # list ref for circle and center plots
        bounds = [] ; center = []
        
        # create plot vals 
        for col in range(COL):
            for row in range(ROW):
                
                x1, y1 = (cell*row)+offset, (cell*col)
                x2, y2 = (x1+cell), (y1+cell)
                x3, y3 = (x1+midd), (y1+midd)

                bounds.append((x1, y1, x2, y2))
                center.append((x3, y3))

        # create button canvas items
        for i in range(MATRIX_SIZE):

            self.button.append( 
                self.create_oval( 
                    bounds[i],
                    outline='black',
                    width=10,
                    tags=tag.button[i]
                )
            )
            self.button_txt.append(
                self.create_text( 
                    center[i], fill='black', 
                    font=self.font, justify='left', 
                    tags=tag.button_txt[i]
                )
            )
            self.button_img.append(
                self.create_image( 
                    center[i], 
                    image=self.button_avatars[i],
                    state='hidden',
                    tags=tag.button_img[i]
                )
            )
    
    def create_side_panels(self, width, height):
        '''

        Create canvas left / right panel items.
        Panels to left and right side of square
        centered on screen.
        Dims are ratio based off parent frame
        text and images centered at 1/4 positions
        of frame height.
        
        :param width: parent frame width
        :param height: parent frame height
        
        '''
        
        # x plot val, width from screen
        # edge to center square
        width_offset = (width-height) / 2
        
        # mid y plot vals
        # 1/4, 1/2, 3/4
        middle = height / 2
        top_mid = middle / 2
        bot_mid = height-(middle/2)
        
        # left panel plot val
        rec_bounds = (0, 0, width_offset, height)
        
        # create left panel
        self.left_rec = self.create_rectangle(rec_bounds, fill='black')
        
        # plot vals for left text, image
        left_mid = width_offset / 2
        mid_bounds = (left_mid, middle)
        top_bounds = (left_mid, top_mid)
        bot_bounds = (left_mid, bot_mid)
        
        # create left panel text, images
        self.left_mid_txt = self.create_text(mid_bounds,
                                             fill='white',
                                             font=self.font)
        
        self.left_top_txt = self.create_text(top_bounds,
                                             fill='white',
                                             font=self.font)
        
        self.left_bot_txt = self.create_text(bot_bounds,
                                             fill='white',
                                             font=self.font)
        
        self.left_mid_img = self.create_image(mid_bounds, image=None)
        
        self.left_top_img = self.create_image(top_bounds, image=None)
        
        self.left_bot_img = self.create_image(bot_bounds, image=None)
        
        
        # right zero is starting point
        # from right edge screen to centered square
        right_zero = width - width_offset
        
        # right panel plot val
        rec_bounds = (right_zero, 0, width, height)
        
        # create right panel
        self.right_rec = self.create_rectangle(rec_bounds, fill='black')
        
        # plot vals for right text, image
        right_mid = width - left_mid
        mid_bounds = (right_mid, middle)
        top_bounds = (right_mid , top_mid)
        bot_bounds = (right_mid, bot_mid)
        
        # create right panel text, images
        self.right_mid_txt = self.create_text(mid_bounds,
                                              fill='white',
                                              font=self.font)
        
        self.right_top_txt = self.create_text(top_bounds,
                                              fill='white',
                                              font=self.font)
        
        self.right_bot_txt = self.create_text(bot_bounds,
                                              fill='white',
                                              font=self.font)
        
        self.right_mid_img = self.create_image(mid_bounds, image=None)
        
        self.right_top_img = self.create_image(top_bounds, image=None)
        
        self.right_bot_img = self.create_image(bot_bounds, image=None)
    
            
            
    
    async def set_panel_info(self, clear, guess, score, name, img_index):
        '''
        Set and clear panel items. Uses direct reference to
        panel variables, e.g, self.left_panel_txt
        
        ** MAY BE CHANGED: Currently panel item positions are
            - left_top for text info: name, score, guess
            - left_bot for avatar image
        ** IF CHANGED UPDATE INFO 
        
        :param clear: if True, hides panel items
        :param guess: number of guesses left in game
        :param score: player score value
        :param name: player name
        :param img_index: chooses what avatar will be shown
        
        * params sent by controller
        '''
        
        # helps with concurrency
        await asyncio.sleep(self.interval)
        
        if clear is True:
            self.itemconfig(self.left_top_txt, state='hidden')
            self.itemconfig(self.left_bot_img, state='hidden')
        
        else:
            
            # show avatar if chosen
            if img_index is not None:
                img = self.panel_avatars[img_index]
                self.itemconfig(self.left_bot_img, state='normal', image=img)  
            
            if guess is not None:
                
                # displayed panel info if quickplay is chosen
                # e.g, player has not selected avatar and name
                if name is None:
                    info = ('SCORE: %s\n\n\nGUESS: %s' % (str(score), str(guess)))
                
                # show full info
                else:
                    info = ('NAME: %s\n\nSCORE: %s\n\n\nGUESS: %s' % (name, str(score), str(guess)))
            else:
                info = ''
            
            # set text info
            font_type, size, style = self.font
            size -= 10
            font = (font_type, size, style)
            self.itemconfig(self.left_top_txt,
                            state='normal',
                            text=info,
                            font=font)
                            


    
    def clear(self):
        '''
        Set button and background items to state='hidden 
        Unpacks dict and containing tags
        See config.py for more info
        '''
        
        for key,value in self.clear_config.items():
            self.itemconfig(**value)


    def set_config(self, config, clear_screen=False):
        '''
        Set button / background text items
        
        :param config: itemconfig settings, sent as dict
        :param clear_screen: resets items if needed
        '''
        
        if clear_screen == True:
            self.clear()
        for key,value in config.items():
            self.itemconfig(**value)


    async def set_color(self, color_string):
        '''
        Sets button matrix colors.
        Refs dict containing colors (see color.py)
        
        :param color_string: 9 character string
            compares characters to color dict
        '''
        
        # helps with concurrency
        await asyncio.sleep(self.interval)
        
        # clears items before setting
        self.clear()
        
        # compare color_string to dict
        for i, letter in enumerate(color_string):
            if letter in color.ColorDict:
                button_color = color.ColorDict[letter] 
            else:
                button_color = color.ColorDict['default color']
            self.itemconfig(self.button[i],fill=button_color, state='normal')


    async def updater(self):
        '''
        Updates canvas at a rate of self.interval
        Added to asyncio loop for continuous update
        '''
        
        while True:  
            self.update()
            await asyncio.sleep(self.interval)