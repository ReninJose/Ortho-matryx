# Authors: Ellis Hobbby, Ryan White
# Version: 3.0


import tkinter as tk
import asyncio as io
import gui
#from ble import OrthoMatryxBLE

from util.timer  import timed
from util.player import Player
from util.config import GenericConfig
from util.color  import DEFAULT, ColorDict

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
        
        # BLE control Object
        #self.dev = OrthoMatryxBLE()
            
        # Vars for tracking model states
        #self.reset_game_data()

        # GUI View objects
        self.gui     = self._gui_init()
        self.avatar  = self.gui.panel_avatars
        self.view    = GenericConfig(self).view.copy()
        
        self.model   = None
        self._model  = {
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
        Model.ctrl = self
        
        # Create async loop
        self.flag  = io.Event()
        self.loop  = io.get_event_loop()
        Model.loop = self.loop
        task = self.loop.create_task(self.run())
        
        try:
            self.loop.run_until_complete(task)
        except Exception as err:
            print(err)


#---------------------------------------------
    
#    Initializer: Canvas View

#---------------------------------------------  
    def _gui_init(self):
        '''
        Initialize canvas display
        
        :return: GUI obj
        
        '''
        self.title("Ortho-Matryx Game")
        
        # get root screen dims and set root geometry
        dims = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%sx%s" % (dims))
        
        self.width, self.height = dims

        self.config = GenericConfig(self)

        # create, pack, update frame
        frame = tk.Frame(self, bg='black')
        frame.pack(fill=tk.BOTH, expand=tk.YES)
        frame.update()

        return gui.GUI(frame, self)
    

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
    async def _show(self, event):
        
        await event.wait()
        
        await io.gather(self._set_view(), self._set_color(), self._set_info())
        
        self.flag.clear()
        self.loop.create_task(self._show(self.flag))       
                

    
    
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
            


                
                
    
    async def _updater(self):
        '''
        Updates canvas at a rate of self.interval
        Added to asyncio loop for continuous update
        '''
        while True:  
            self.gui.update()
            await io.sleep(1/120)

        
        
#---------------------------------------------
    
#    Event Binding Functionality

#---------------------------------------------

    def set_event(self, buttons=None, obj=None, func=None):
        '''
        Binds user inputs to dispatch a specific model
        
        :param buttons: the inputs to bind
        :param func: the function to call on button event
        :param dispatch: model object to dispatch on event
        
        '''
        _obj = self._model[obj]

        for key in buttons:
            if obj:
                self.bind(key, lambda event: _obj(event.keysym))
            else:
                self.bind(key, lambda event: func(event.keysym))


    def remove_event(self):
        '''
        Removes all button event binds
        
        '''
        for binding in USER_INPUTS:
            self.unbind(binding)


    def dispatch(self, obj):
        _obj = self._model[obj]
        _obj()
        

#---------------------------------------------
    
#    BLE Functionality

#---------------------------------------------

    async def ble_tx(self, color_string):
        '''
        BLE TX for color data
        
        :param color_string: the color data
        
        '''
        # Comment below for dev w.o BLE
        #self.dev.tx_rgb(color_string)
        pass
    
    async def ble_scan(self):
        '''
        BLE Scan and Connect:
        Continuosly scans for peripheral
        Once found, attempts to connect
        and listens for incoming RX data
        
        '''
        # Comment below for dev w.o BLE
        """
        scan = await self.dev.scan()
        if scan:
            await self.dev.connect()
            
            while self.dev.status():
                await asyncio.sleep(5)
        else:
            menus.TitleScreen(self)
        """
        pass
            
            
#---------------------------------------------
    
#    Async Loop Functionality

#---------------------------------------------

    async def run(self):
        '''
        Creates the main asycio loop
        If not peripheral connected
        will continously call ble.scan
        
        '''
        self.loop.create_task(self._show(self.flag))
        self.loop.create_task(self._updater())
        self.model = TitleScreen(self)

        while True:
            await self.ble_scan()
            await io.sleep(1)
            
        
  

            
app = App()


