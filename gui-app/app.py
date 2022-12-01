# Authors: Ellis Hobbby, Ryan White
# Version: 3.0


import tkinter as tk
import asyncio as io
import pygame.mixer as mixer
mixer.init()


import gui

from ble import BLE

from util.timer  import timed
from util.player import Player
from util.config import GenericConfig
from util.color  import DEFAULT, ColorDict
from util.path   import *

from model.model import Model
from model.mem   import MemoryGame
from model.tic   import TicTacToe
from model.pig   import PigDice

from model.menus import (TitleScreen, MainMenu, GameSelect, 
AvatarMenu, PlayerName, StartButton, PostGameMenu, HighScoreScreen)




"""---------------------------------------------
    
    IMPORTANT INFO:

    * Must change paths in /util/path.py *
    
    * For dev without ble functionality *
    
        > Comment out: ble_tx() and ble_scan()
    

---------------------------------------------"""

# GUI event bindings
USER_INPUTS = (
    '<q>', '<w>', '<e>',
    '<a>', '<s>', '<d>',
    '<z>', '<x>', '<c>'
)

# Used for adjusting text size ratio
DEV_SCREEN_WIDTH = 1920


FONT = 'Atari Font Full Version'



class App(tk.Tk):
    '''
    Main Application. Serves as controller.
    Inherits from tkinter root
    Enables concurrency using asyncio
    
    > Creates view object from gui.py
        > Controls gui screen output
            - text, color, image
        
    > Creates BLE control object from ble.py
        > Scans, connect
        > TX color data
        > RX button inputs
        
        
    > Dispatch model objects for menus and game
        > Responds to gui and ble control requests
    
    
    > Adds GUI and BLE tasks to asyncio loop
    '''
    
    def __init__(self, *args, **kwargs):
        super().__init__()

        # Initialize
        self._gui_init()
        self._model_init()
        self._sound_init()

        # Bind cleanup on prog win closed
        self.bind('<Destroy>', self.cleanup)
        self.bind('<Escape>', lambda event: self.destroy())
        
        # aysnc event flags
        self.show_flag  = io.Event()
        self.idle_flag = io.Event()
        self.active_flag = io.Event()
        
        # get main loop
        self.loop  = io.get_event_loop()

        # set model loop
        Model.loop = self.loop

        # BLE control obj
        # send loop and connect startup color (main menu)
        self.ble = BLE(self, self.loop, 'GxGxBxRxW')

        # being program loop, handle errors, clean shutdown
        try:
            self.loop.run_until_complete(self.loop.create_task(self.run()))
        except io.CancelledError as err:  
            pass
        finally:
            self.loop.close()


#---------------------------------------------
    
#    Cleanup Sequence

#---------------------------------------------          
    def cleanup(self, event):
        '''
            on program shutdown:
            stop button and music sounds
            disconnect ble device
            cancel any pending async tasks
        '''
        self.button_mixer.stop()
        self.music.stop()
        self.loop.create_task(self.ble.disconnect())
     
        for task in io.all_tasks():
            try:
                task.cancel()
            except io.CancelledError as err:  
                pass 
            

#---------------------------------------------
    
#    Initializer: Canvas View

#---------------------------------------------  
    def _gui_init(self):
        '''
        Initialize canvas display
        
        '''
        # set main win title
        self.title("Ortho-Matryx Game")
        
        # get root screen dims and set root geometry
        self.width, self.height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%sx%s" % (self.width, self.height))
        self.attributes('-fullscreen', True)

        # help with config settings
        self.config = GenericConfig(self)
        self.view  = GenericConfig(self).view.copy()

        # create, pack, update frame
        frame = tk.Frame(self, bg='black')
        frame.pack(fill=tk.BOTH, expand=tk.YES)
        frame.update()
        
        # ref to GUI canvas objs
        self.gui = gui.GUI(frame, self)

        # ref for different avatar placements
        self.panel_avatar = self.gui.panel_avatars
        self.score_avatar = self.gui.score_avatars

        # Ref for current color of GUI buttons
        self.color = ''
    


#---------------------------------------------
    
#    Initializer: Main/Sub Model 

#---------------------------------------------  
    def _model_init(self):
    
        # Ref for GUI Model
        self.model = None

        # Template for GUI Model objs
        self.template  = {
            'title-screen': TitleScreen,
            'main-menu'   : MainMenu,
            'game-select' : GameSelect,
            'avatar-menu' : AvatarMenu,
            'player-name' : PlayerName,
            'start-button': StartButton,
            'post-game'   : PostGameMenu,
            'high-score'  : HighScoreScreen,
            'memory'      : MemoryGame,
            'tic-tac-toe' : TicTacToe,
            'pig-dice'    : PigDice,
            None : None
        }

        # Send self for main model controller
        Model.ctrl = self

        # templates are sub models
        Model.sub  = self.template

        # Dict for keypress events
        # Will dispatch model obj and funcs
        self.event_dict = {}



#---------------------------------------------
    
#    Initializer: Main/Sub Model 

#---------------------------------------------  
    def _sound_init(self):
        
        # dict for button sounds
        # see util.path.py for B1_WAV.. etc
        self.sounds = {
            'q': mixer.Sound(B1_WAV),
            'w': mixer.Sound(B2_WAV),
            'e': mixer.Sound(B3_WAV),
            'a': mixer.Sound(B4_WAV),
            's': mixer.Sound(B5_WAV),
            'd': mixer.Sound(B6_WAV),
            'z': mixer.Sound(B7_WAV),
            'x': mixer.Sound(B8_WAV),
            'c': mixer.Sound(B9_WAV),
        }
        
        # set button channel and vol
        self.button_mixer = mixer.Channel(1)
        self.button_volume = 0.75
        
        # set/load music and vol
        self.music = mixer.music
        self.music.load(THEME_WAV)
        self.music_volume = 0.5    



#---------------------------------------------
    
#    Canvas Control Functionality

#---------------------------------------------
    def set_font(self, font=FONT, size=30, style='normal'):
        '''
        Enables the font settings to be altered.
        Ratios font size based off parent frame
        
        :param font: font type, default='Atari Font Full Version'
        :param size: font size, default=35
        :param style: font style, default='normal'
        
        :return: font settings tuple
        
        '''
        
        # create font size ratio
        screen_width = self.width
        size_ratio = screen_width / DEV_SCREEN_WIDTH
        size = int(size_ratio * size)
        
        return (font, size, style)

               
            
    #@timed('orange')
    async def _show(self):
        
        await self.show_flag.wait()
        
        await io.gather(self._set_view(), self._set_color(), self._set_info())
        
        self.show_flag.clear()
        self.loop.create_task(self._show())       
                
    
    #@timed('purple')
    async def _set_view(self, **kwargs):
        
        await io.sleep(1/120)

        for tag, args in self.model.config.items():
            self.view[tag]['state'] = 'normal'
            for opt, val in args.items():
                self.view[tag][opt] = val     

        for key,value in self.view.items():
            self.gui.itemconfig(key, **value)
            
        self.view = GenericConfig(self).reset.copy()
    
        
    #@timed('cyan')    
    async def _set_color(self):

        await io.sleep(1/120)
        
        if self.color != self.model.color:
            if self.model.color == None: 
                self.loop.create_task(self.ble.send_data('XXXXXXXXX'))
            else:
                self.loop.create_task(self.ble.send_data(self.model.color))
            self.color = self.model.color

        if self.model.color is not None:    
            for i, letter in enumerate(self.model.color):
                if letter in ColorDict:
                    button = ColorDict[letter] 
                else:
                    button = DEFAULT

                self.gui.itemconfig( self.gui.button[i],
                                     state='normal', 
                                     fill=button )
                    
    #@timed('blue')      
    async def _set_info(self):

        await io.sleep(1/120)
        
        if self.model.game_run is True:

            self.gui.itemconfig(**self.model.active_player['TEXT'])
            self.gui.itemconfig(**self.model.active_player['IMAGE'])

            self.gui.itemconfig('player-rec-clear', state='hidden')

            if self.model.highlight == 1:
                self.gui.itemconfig('player-1-rec',state='normal')

            elif self.model.highlight == 2:
                self.gui.itemconfig('player-2-rec',state='normal')

        else:
            self.gui.itemconfig('player-txt-clear', text='', state='hidden')
            self.gui.itemconfig('player-img-clear', image='', state='hidden')
            self.gui.itemconfig('player-rec-clear', state='hidden')
                   
    
    async def _updater(self):
        '''
        Updates canvas at a rate of self.interval
        Added to asyncio loop for continuous update
        '''
        while True:  
            self.gui.update()
            await io.sleep(1/120)


#---------------------------------------------
    
#    Sound Control Functionality

#---------------------------------------------

    def button_sounds(self, key):
        self.button_mixer.set_volume(self.button_volume)
        
        # attempt to play relevant sound from key
        # key obtained from ble notification
        try:
            self.button_mixer.play(self.sounds[key])
        except:
            pass
        
              
                
    def theme_song(self, play=False):
        
        self.music.set_volume(self.music_volume)
        
        if not play and self.music.get_busy():
            self.music.fadeout(2000)
            
        elif not self.music.get_busy() and play:
            self.music.play(loops=-1)
        
        
#---------------------------------------------
    
#    Event Binding Functionality

#---------------------------------------------

    def model_event(self, key):
        '''
            event keys retrieved from
            ble notification data
        '''
        event_key = f'<{key}>'
        if event_key in self.event_dict:
            event = self.event_dict[event_key]
            event(key)    
        self.button_sounds(key)


    def dispatch(self, obj):
        self.template[obj]()
               
            
            
#---------------------------------------------
    
#    Async Loop Functionality

#---------------------------------------------

    async def run(self):
        '''
        Creates the main asycio loop
        
        '''
        self.loop.create_task(self._show())
        self.loop.create_task(self._updater())
        
        while True:
            
            # these flags are set and cleared by ble class
            # helps synchonize gui to ble controller
            self.model = TitleScreen()
            await self.idle_flag.wait()
            
            self.model = MainMenu()
            await self.active_flag.wait()
            
        
  
        
app = App()


