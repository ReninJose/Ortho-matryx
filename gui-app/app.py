# Authors: Ellis Hobbby, Ryan White
# Version: 2.0


import tkinter as tk
import asyncio
import gui
#from ble import OrthoMatryxBLE
import menus
from PIL import Image, ImageTk
from util import path


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
        
        # Vars for tracking model states
        self.game_running = False
        self.quickplay = False
        self.avatar_index = None
        self.name = None
        self.score = 0
        self.total = 0
        
        
        # BLE control Object
        #self.dev = OrthoMatryxBLE()
        
        
        # GUI View objects
        self.frame = self.frame_init()
        self.font = self.set_font()
        self.gui = self.gui_init()
        
        
        # List ref for event bindings
        self.binding = []
        
        
        # Create async loop
        self.loop = asyncio.get_event_loop()
        task = self.loop.create_task(self.run())
        try:
            self.loop.run_until_complete(task)
        except Exception as err:
            print(err)
        finally:
            print('done')
            


#---------------------------------------------
    
#    Initializer: Frame and Canvas View

#---------------------------------------------

            
    def frame_init(self):
        '''
        Initialize the main parent frame
        Frame size based off screen dims
        
        :return: tkinter frame
        
        '''
        
        self.title("Ortho-Matryx Game")
        
        # get root screen dims and set root geometry
        dims = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%sx%s" % (dims))
        
        # create, pack, update, and return frame
        frame = tk.Frame(self, bg='black')
        frame.pack(fill=tk.BOTH, expand=tk.YES)
        frame.update()
        return frame
    
    
    def gui_init(self):
        '''
        Initialize canvas display
        
        :return: GUI obj
        
        '''
        return gui.GUI(self.frame, self.font)
    

#---------------------------------------------
    
#    Canvas Control Functionality

#---------------------------------------------

    def set_font(self, font='Atari Font Full Version', size=35, style='normal'):
        '''
        Enables the font settings to be altered.
        Ratios font size based off parent frame
        
        :param font: font type, default='Atari Font Full Version'
        :param size: font size, default=35
        :param style: font style, default='normal'
        
        :return: font settings tuple
        
        '''
        
        # create font size ratio
        screen_width = self.frame.winfo_screenwidth()
        size_ratio = screen_width / DEV_SCREEN_WIDTH
        size = int(size_ratio * size)
        
        return (font, size, style)
    

    async def update_gui(self, configs, color=None, clear=False):
        '''
        Control for canvas color and config settings
        
        :param configs: sent as dict containing
                        configs and canvas item tags
        :param color: color string for matrix
                      buttons, default=None
        :param clear: bool for config clear
                      sets item state='hidden'
                      default=False
                      
        '''
                      
        if color is not None:
            await self.gui.set_color(color)
        if configs is not None:
            self.gui.set_config(configs, clear)
          
    
    async def show_player_info(self, clear=False, remaining=None):
        '''
        Control for canvas side panel items
        
        :param clear: bool for config clear
                      sets item state='hidden'
                      default=False
        :param remaining: player guess remaining
                          during gameplay
                          default=None
        '''
        await self.gui.set_panel_info(clear, remaining, self.total, self.name, self.avatar_index)
        

    
    async def clear_player_info(self):
        '''
        Clears canvas side panel items
        
        '''
        await self.show_player_info(clear=True)
        
        
#---------------------------------------------
    
#    Event Binding Functionality

#---------------------------------------------

    def set_event_bind(self, buttons, func, dispatch=None):
        '''
        Binds user inputs to dispatch a specific model
        
        :param buttons: the inputs to bind
        :param func: the function to call on button event
        :param dispatch: model object to dispatch on event
        
        '''
        for key in buttons:
            if dispatch:
                self.binding.append(self.bind(key, lambda event: asyncio.ensure_future(func(dispatch))))
            else:
                self.binding.append(self.bind(key, lambda event: asyncio.ensure_future(func(event.keysym))))

    def remove_event_bind(self):
        '''
        Removes all button event binds
        
        '''
        for binding in USER_INPUTS:
            self.unbind(binding)

    async def obj_dispatch(self, dispatch):
        '''
        Dispatches a model object
        
        :param dispatch: the model to be created
        
        '''
        dispatch(self)
        

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
        self.loop.create_task(self.gui.updater())
        menus.TitleScreen(self)

        while True:
            await self.ble_scan()
            await asyncio.sleep(1)
            
        
  

            
app = App()
