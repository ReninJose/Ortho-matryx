# Authors: Ellis Hobbby, Ryan White
# Version: 2.0


import tkinter as tk
from PIL import Image, ImageTk
from util.path import AVATAR_PATH


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
    
    > Items controlled using item tags sent as dictionaries (see config.py)
    
    > Asychronous updates every 1/120 seconds
    
    :param parent: tkinter frame obj sent from controller
    '''
    
    def __init__(self, parent, controller):
        
        height = parent.winfo_height()
        width = parent.winfo_width()
        
        # create inherited canvas using screen dimensions of parent frame
        super().__init__(parent, width=width, height=height, bg = 'black', highlightthickness=0)
        self.pack()
        
        self.control  = controller
        self.config   = controller.config.view
        self.player   = controller.config.player
        
        # reference for button images
        self.button_avatars=[]

        # reference for panel images
        self.panel_avatars=[]

        self.score_avatars=[]
        
        # reference for button id
        self.button=[] 

        # default font settings
        self.bg_font   = controller.set_font(style='italic')
        self.btn_font  = controller.set_font()
        self.panl_font = controller.set_font(size=18)
        self.titl_font = controller.set_font(size=25)
        self.fname, self.fsize, self.fstyle = self.font = controller.set_font()
        

        # initate all canvas items
        self._upload_avatars    (width, height)
        self._create_background (width, height)
        self._create_highscore  (width, height)
        self._create_buttons    (width, height)
        self._create_panels     (width, height)

        
        
    def _upload_avatars(self, width, height):
        '''

        Upload avatar images and resize accordingly.
        Added to avatar lists for reference.
        
        :param width: parent frame width
        :param height: parent frame height
        
        ''' 
        # image size for buttons
        b_size = int(height / 5)
        
        # image size for panels
        self.p_size = int((width-height) / 2)

        s_size = int(height / 4)
        
        
        # upload and create panel / button images
        for i in range(6):
            b_img = (Image.open(AVATAR_PATH + str(i) + '.png').resize((b_size,b_size)).convert('RGBA'))
            p_img = (Image.open(AVATAR_PATH + str(i) + '.png').resize((self.p_size,self.p_size)).convert('RGBA'))
            s_img = (Image.open(AVATAR_PATH + str(i) + '.png').resize((s_size,s_size)).convert('RGBA'))
            self.button_avatars.append(ImageTk.PhotoImage(b_img))
            self.panel_avatars.append(ImageTk.PhotoImage(p_img))
            self.score_avatars.append(ImageTk.PhotoImage(s_img))


        # fill extra list space button_avatars
        # will run into problems if it does
        # not equal matrix size (9)
        for i in range(3):
            self.button_avatars.append(None)
            
            
    def _create_background(self, width, height):
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
        x2 = height + offset; y2 = height
        
        # plot vals for background text, image
        x3 = width / 2; y3 = height / 2
        
        # create tuples for plot vals
        bounds = (x1, y1, x2, y2)
        center = (x3, y3)
        
        
        # creating background items
        self.create_rectangle( 
                bounds,
                **self.config['bg']
        )
        self.create_text( 
            center,
            **self.config['bg-txt']
        )
        self.create_image(
            center,
            **self.config['bg-img']
        )

    def _create_highscore(self, width, height):
        
        _row = 3; _col = 4

        label_y = self.fsize * 4
        midd_l  = label_y / 2

        cell_x  = width / 4
        cell_y  = (height-label_y) / 3

        midd_x  = cell_x / 2
        midd_y  = cell_y / 2

        for col in range(_col):

            x1, y1 = (cell_x*col), 0
            x2, y2 = (x1+cell_x), label_y
            dims   = (x1, y1, x2, y2)
            midd   = (x1+midd_x) , (y1+midd_l)

            self.create_rectangle(dims, **self.config['sb-grid'])
            
            self.create_text(midd, **self.config[f'sb-label-{col}'])


        tag = [ 'sb-rank-{}', 'sb-name-{}', 'sb-score-{}', 'sb-avatar-{}']

        for row in range(_row):
            for col in range(_col):
                
                _tag_1 = tag[col].format(row)
                _tag_2 = tag[col].format(row+3)
                _tag_3 = tag[col].format(row+6)
                
                x1, y1 = (cell_x*col), (cell_y*row)+label_y
                x2, y2 = (x1+cell_x) , (y1+cell_y)
                x3, y3 = (x1+midd_x) , (y1+midd_y)

                bounds = (x1, y1, x2, y2)
                center = (x3, y3)

                self.create_rectangle(bounds, **self.config['sb-grid'])

                if col == 3:
                    self.create_image(center, **self.config[_tag_1])
                    self.create_image(center, **self.config[_tag_2])
                    self.create_image(center, **self.config[_tag_3])
                else:
                    self.create_text(center, **self.config[_tag_1])
                    self.create_text(center, **self.config[_tag_2])
                    self.create_text(center, **self.config[_tag_3])
                
            

        
    def _create_buttons(self, width, height):
        '''

        Create canvas button items.
        3x3 matrix of perfect circles.
        Based off square centered on screen.
        text and images centered on circles
        
        :param width: parent frame width
        :param height: parent frame height
        
        '''
        h_offset = self.fsize * 2
        height   = height - (h_offset * 2)
        
        # helps center items in square 
        # background based off screen height
        w_offset = (width-height) /2
        
        # val for matrix cell dimension
        cell = (height / 3)
        
        # middle point of each cell
        midd = cell / 2
        
        # list ref for circle and center plots
        bounds = [] ; center = []
        
        # create plot vals 
        for col in range(COL):
            for row in range(ROW):
                
                x1, y1 = (cell*row)+w_offset, (cell*col)+h_offset
                x2, y2 = (x1+cell), (y1+cell)
                x3, y3 = (x1+midd), (y1+midd)

                y1 += h_offset; y2 += h_offset; y3 += h_offset

                bounds.append((x1, y1, x2, y2))
                center.append((x3, y3))

        # create button canvas items
        for i in range(MATRIX_SIZE):

            self.button.append( 
                self.create_oval( 
                    bounds[i],
                    **self.config[f'btn-{i}']
                )
            )
            self.create_text( 
                center[i], 
                **self.config[f'txt-{i}']
            )
            self.create_image( 
                center[i], 
                image=self.button_avatars[i],
                **self.config[f'img-{i}']
            )

    
    def _create_panels(self, width, height):
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
        x0 = self.p_size / 2
        y0 = ((height - self.p_size) / 2) + self.p_size

        x1 = self.fsize * 2
        y1 = self.fsize * 4
        
        x2 = width - x1
        y2 = height - y1

        x3 = 10
        y3 = 10

        x4 = ((width-height)/2) - 10
        y4 = height - 10

        left_top  = (x1, y1)
        left_bot  = (x0, y0)
        left_rec  = (x3, y3, x4, y4)

        self.create_rectangle(
            left_rec,
            **self.player['player-1-rec']
        )  
        self.create_text(
            left_top, 
            **self.player['player-1-txt']
        ) 
        self.create_image(
            left_bot, 
            **self.player['player-1-img']
        )

        x0 = width - x0
        
        x3 = (width - ((width-height)/2)) + 10
        y3 = 10

        x4 = width - 10
        y4 = height - 10
        
        right_top = (x2, y1)
        right_bot = (x0, y0)
        right_rec = (x3, y3, x4, y4)

        self.create_rectangle(
            right_rec,
            **self.player['player-2-rec'] 
        ) 
        self.create_text(
            right_top,
            **self.player['player-2-txt']
        )     
        self.create_image(
            right_bot, 
            **self.player['player-2-img']
        )


        x = width / 2
        y = self.fsize * 2
        top_mid = (x, y)        

        self.create_text(
            top_mid,
            **self.config['title']
        )
