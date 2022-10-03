# Authors: Ellis Hobbby, Ryan White
# Version: 2.0


import asyncio
import subprocess
from util import config, path, color
from game import PlayGame as Game


"""---------------------------------------------
    
    IMPORTANT INFO:

    * Must change paths in /util/path.py *
    

---------------------------------------------"""



#-----------------------------------------------------

#    Title Screen

#-----------------------------------------------------

class TitleTools:
    '''
    Constants for TitleScreen
    
    COLOR_MAP: Button matrix colors
    MAIN_MENU: Event - Menu Dispatch
    
    '''
    COLOR_MAP = 'RGBWWRGWB'
    
    MAIN_MENU = (
        '<q>', '<w>', '<e>',
        '<a>', '<s>', '<d>',
        '<z>', '<x>', '<c>'
    )

class TitleScreen(TitleTools):
    '''
    TitleScreen Model Object
    Will be shown when BLE peripheral
    not connected and game is idle
    
    Dispatches MainMenu on button event
    
    :param controller: Main App controller
    
    '''
    def __init__(self, controller):
        
        # save controller and remove event binds
        self.controller = controller
        controller.remove_event_bind()
        
        # set canvas view configs
        settings = (
            ('ortho', {'text': 'ORTHO'}), 
            ('matryx', {'text': 'MATRYX'}), 
            ('game', {'text': 'GAME'})  
        )
        self.config = config.GenericConfig('title', 'normal', settings).configs
        
        # reset game state vars in controller
        controller.name = None
        controller.score = 0
        controller.total = 0
        controller.avatar = None
        controller.game_running = False 
        controller.quickplay = True 
        
        # set event binds and add model view to async loop
        controller.set_event_bind(self.MAIN_MENU, controller.obj_dispatch, MainMenu)
        controller.loop.create_task(self.show())

    async def show(self):
        '''
        Show model view
        TX RGB color data
        
        '''
        await self.controller.clear_player_info()
        await self.controller.ble_tx(self.COLOR_MAP)
        await self.controller.update_gui(self.config, self.COLOR_MAP)
        


#-----------------------------------------------------

#    Menu Screen

#-----------------------------------------------------

class MenuTools:
    '''
    Constants for MainMenu
    
    COLOR_MAP: Button matrix colors
    
    AVATAR_MENU: Event - AvatarMenu Dispatch
    PLAY_GAME:   Event - PlayGame Dispatch
    QUIT_GAME:   Event - TitleScreen Dispatch
    HIGH_SCORE:  Event - HighScoreScreen Dispatch
    
    '''
    COLOR_MAP = 'GXBXXXRXW'
    AVATAR_MENU = ['<e>']
    PLAY_GAME = ['<q>']
    QUIT_GAME = ['<z>']
    HIGH_SCORE = ['<c>']
       

class MainMenu(MenuTools):
    '''
    MainMenu Model Object
    Dipatch on events to:
    quickplay, avatar menu, exit, high scores
    
    :param controller: Main App controller
    
    '''
    def __init__(self, controller):
        
        # save controller and remove event binds
        controller.remove_event_bind()
        self.controller = controller
        
        # set canvas view configs
        settings = (
            ('avatar', {'text': 'AVATAR\nSELECT'}), 
            ('play', {'text': 'QUICK\nPLAY'}),
            ('quit', {'text': 'EXIT\nGAME'}),  
            ('score', {'text': 'HIGH\nSCORES'}),    
        )
        self.config = config.GenericConfig('menu', 'normal', settings).configs
        
        # reset game state vars in controller
        controller.name = None
        controller.score = 0
        controller.total = 0
        controller.avatar_index = None
        controller.game_running = False 
        controller.quickplay = True        
        
        # set event binds and add model view to async loop
        controller.set_event_bind(self.AVATAR_MENU, controller.obj_dispatch, AvatarMenu)
        controller.set_event_bind(self.PLAY_GAME, controller.obj_dispatch, StartButton)
        controller.set_event_bind(self.QUIT_GAME, controller.obj_dispatch, TitleScreen)
        controller.set_event_bind(self.HIGH_SCORE, controller.obj_dispatch, HighScoreScreen)
        controller.loop.create_task(self.show())


    async def show(self):
        '''
        Show model view
        TX RGB color data
        
        '''
        await self.controller.clear_player_info()
        await self.controller.ble_tx(self.COLOR_MAP)
        await self.controller.update_gui(self.config, self.COLOR_MAP)


#-----------------------------------------------------

#    Avatar Screen

#-----------------------------------------------------

class AvatarTools:
    '''
    Constants for AvatarMenu
    
    COLOR_MAP_1: Button colors before selection
    COLOR_MAP_2: Button colors during selection
                 updated to highlight current
    
    SELECT:      Event - Updates COLOR_MAP_2
    MAIN_MENU:   Event - MainMenu Dispatch
    ENTER_NAME:  Event - PlayerName Dispatch
    
    KEY_TO_NUM: Dict to translate event keys
                to avatar image index vals
    
    '''
    COLOR_MAP_1 = 'BBBBBBRXX'
    COLOR_MAP_2 = 'XXXXXXRXG'

    SELECT = ['<q>', '<w>', '<e>', '<a>', '<s>', '<d>']
    MAIN_MENU = ['<z>'] 
    ENTER_NAME = ['<c>']

    KEY_TO_NUM = {
        'q': 0,
        'w': 1,
        'e': 2,
        'a': 3,
        's': 4,
        'd': 5,
        'z': 6,
        'x': 7,
        'c': 8
    }


class AvatarMenu(AvatarTools):
    '''
    AvatarMenu Model Object
    Dipatch on events to:
    avatarselection(), MainMenu, PlayerName
    
    :param controller: Main App controller
    
    '''
    
    def __init__(self, controller):
        
        # save controller and remove event binds
        controller.remove_event_bind()
        self.controller = controller
        
        # set canvas view configs
        settings  = (
            ('back', {'text':'MAIN\nMENU'}), 
            ('play', {'text':''}),
            ('0', {}),
            ('1', {}),
            ('2', {}),
            ('3', {}),
            ('4', {}),
            ('5', {})       
        )
        self.config = config.GenericConfig('avatar', 'normal', settings).configs
        
        # if we have reached this model,
        # the game is not in quickplay
        # update the controller state
        controller.quickplay = False
        
        # set event binds for MainMenu and avatar_selection
        # PlayerName bind is set after avart_selection has started
        # add model view to async loop
        controller.set_event_bind(self.MAIN_MENU, controller.obj_dispatch, MainMenu)
        controller.set_event_bind(self.SELECT, self.avatar_selection)
        controller.loop.create_task(self.show())


    async def show(self):
        '''
        Show model view
        TX RGB color data
        
        '''
        await self.controller.ble_tx(self.COLOR_MAP_1)
        await self.controller.update_gui(self.config, self.COLOR_MAP_1)

    async def avatar_selection(self, key):
        '''
        Each time a player presses an avatar spot,
        its button space is highlighted and its
        index value is updated in the controller.
        
        PlayerName Event is now dispatched
        
        :parap key: the key pressed during event
                    translated to index value
                    using KEY_TO_NUM dict
        
        '''
        # enter name is now available
        # update this visually
        self.config['play']['text'] = 'ENTER\nNAME'
        
        # translate key to index value
        selection = self.KEY_TO_NUM[key]
        
        # add index value to controller
        self.controller.avatar_index = selection
        
        # update the color map to highlight selection
        select_color = self.COLOR_MAP_2[:selection] + 'B' + self.COLOR_MAP_2[selection+1:]
        
        # update BLE RGB and canvas view
        await self.controller.ble_tx(select_color)
        await self.controller.update_gui(self.config, select_color)
        
        # enable PlayName event to be called
        self.controller.set_event_bind(self.ENTER_NAME, self.controller.obj_dispatch, PlayerName)


#-----------------------------------------------------

#    Player Name Enter Screen

#-----------------------------------------------------

class PlayerNameTools:
    '''
    Constants for PlayerName
    
    COLOR_MAP: Button color matrix
    
    NAME_SELECTION: Event - calls enter_name()

    LETTERS: Used to cycle alphebet for name
    
    '''
    COLOR_MAP = 'WWWXXXRGB'

    NAME_SELECTION = ['<z>', '<x>', '<c>']

    LETTERS = [
        'A', 'B', 'C', 'D', 
        'E', 'F', 'G', 'H', 
        'I', 'J', 'K', 'L', 
        'M', 'N', 'O', 'P', 
        'Q', 'R', 'S', 'T', 
        'U', 'V', 'W', 'X', 
        'Y', 'Z', ' '
    ]


class PlayerName(PlayerNameTools):
    '''
    PlayerName Model Object
    Dipatch on events to:
    enter_name()
    
    :param controller: Main App controller
    
    '''
    def __init__(self, controller):
        
        # save controller and remove event binds
        controller.remove_event_bind()
        self.controller = controller
        
        # update canvas view configs
        settings = (
            ('0', {'text': '', 'font': controller.set_font(size=100)}),
            ('1', {'text': '', 'font': controller.set_font(size=100)}),
            ('2', {'text': '', 'font': controller.set_font(size=100)}),
            ('minus', {'text': '<<<', 'font': controller.set_font(size=60)}),
            ('enter', {'text': 'ENTER'}),  
            ('plus', {'text': '>>>', 'font': controller.set_font(size=60)})     
        )
        self.config = config.GenericConfig('name', 'normal', settings).configs
        
        # used for tracking player name selection
        self.index = len(self.LETTERS) - 1
        self.counter = 0
        self.name = ''
        
        # set event bind and add model to asyncio loop
        controller.set_event_bind(self.NAME_SELECTION, self.enter_name)
        controller.loop.create_task(self.show())

    async def show(self):
        '''
        Show model view
        TX RGB color data
        
        Dispaly selected avatar:
            controller.show_player_info()
        
        '''
        await self.controller.show_player_info()
        await self.controller.ble_tx(self.COLOR_MAP)
        await self.controller.update_gui(self.config, self.COLOR_MAP)

    async def enter_name(self, key):
        '''
        Called during player name sequence
        
        :param key: the key pressed during event
        
        '''
        
        # z moves backwards through the letters
        # decrements the index
        # if index reaches min wrap back
        if key == 'z':
            self.index -= 1
            if self.index == -1:
                self.index = len(self.LETTERS) - 1
        
        # z moves forwards through the letters
        # increments the index
        # if index reaches max wrap back
        if key == 'c':
            self.index += 1
            if self.index == len(self.LETTERS):
                self.index = 0
        
        # uses the current index to display letter
        selected_letter = self.LETTERS[self.index]
        self.config[str(self.counter)]['text'] = selected_letter
        await self.controller.update_gui(self.config)
        
        # x makes a letter selection
        # reset the index
        # update the counter
        # add letter to name
        if key == 'x':
            self.index = -1
            self.name += selected_letter
            self.counter += 1
        
        # if player has selected three letters
        # add player name to canvas panel view
        # dispatch StartButton
        if self.counter == 3:
            self.controller.name = self.name
            await self.controller.show_player_info()
            await self.controller.obj_dispatch(StartButton)
            #subprocess.run([path.BACKEND_PATH, path.BACKED_ARG_SCOREBOARD, self.player_name, str(self.score)])



#-----------------------------------------------------

#    Start Button Screen

#-----------------------------------------------------

class StartButtonTools:
    '''
    Constants for PlayerName
    
    COLOR_MAP: Button color matrix
    
    START: Event - PlayGame Dispatch
    
    '''
    COLOR_MAP = 'XXXXGXXXX'
    START = ['<s>']


class StartButton(StartButtonTools):
    '''
    StartButton Model Object
    Dipatch on events to:
    PlayGame
    
    :param controller: Main App controller
    
    '''
    def __init__(self, controller):
        
        # set controller and remove event binds
        controller.remove_event_bind()
        self.controller = controller
        
        # update canvas view configs
        settings = (
            ('game', {'text':'START\nGAME'}),     
        )
        self.config = config.GenericConfig('start', 'normal', settings).configs
        
        # if in quickplay reset player total to 0
        if controller.quickplay is True:
            controller.total = 0
        
        # set event bind and add model view to asyncio loop
        controller.set_event_bind(self.START, controller.obj_dispatch, Game)
        controller.loop.create_task(self.show())

    async def show(self):
        '''
        Show model view
        TX RGB color data
        
        Display player guess remaing and score:
            controller.show_player_info()
        
        '''
        await self.controller.ble_tx(self.COLOR_MAP)
        await self.controller.update_gui(self.config, self.COLOR_MAP)
        await self.controller.show_player_info(remaining=3)



#-----------------------------------------------------

#    Post Game Menu Screen

#-----------------------------------------------------

class PostGameTools:
    '''
    Constants for PlayerName
    
    COLOR_MAP: Button color matrix
    
    MAIN_MENU:  Event - MainMenu Dispatch
    HIGH_SCORE: Event - HighScoreScreen Dispatch
    PLAY_GAME:  Event - PlayGame Dispatch
    
    '''
    COLOR_MAP = 'WWXXWWRBG'
    MAIN_MENU = ['<z>']
    HIGH_SCORE = ['<x>']
    PLAY_GAME = ['<c>']
    

class PostGameMenu(PostGameTools):
    '''
    PostGameMenu Model Object
    Dipatch on events to:
    MainMenu, HighScoreScreen, PlayGame
    
    :param controller: Main App controller
    
    '''
    def __init__(self, controller):
        
        # set controller and remove event binds
        controller.remove_event_bind()
        self.controller = controller
        
        # update canvas view configs
        settings = [
                ('round', {'text': 'ROUND\nSCORE'}),
                ('score', {'text': controller.score, 'font': controller.set_font(size=80)}),
                ('session', {'text': 'PLAYER\nTOTAL'}),
                ('total', {'text': '', 'font': controller.set_font(size=80)}),
                ('menu', {'text': 'MAIN\nMENU'}),
                ('high', {'text': 'HIGH\nSCORES'}),
                ('play', {'text': 'PLAY\nAGAIN'}),             
        ]
        self.config = config.GenericConfig('post', 'normal', settings).configs
   
        # if not in quickplay, show running total
        # and write to score board
        if controller.quickplay is False:
            self.COLOR_MAP = 'WWXXWWRBG'
            self.config['session']['text'] = 'PLAYER\nTOTAL'
            self.config['total']['text'] = controller.total
            
            # call backend: write player total to score board
            subprocess.run(
                [path.BACKEND_PATH, path.BACKEND_ARG_SCOREBOARD, controller.name, str(controller.total)]
            )
            
        else:
            self.COLOR_MAP = 'WWXXXXRBG'
            self.config['session']['text'] = ''
            self.config['total']['text'] = ''
        
        # set event bind and add model to asyncio loop
        controller.set_event_bind(self.MAIN_MENU, controller.obj_dispatch, MainMenu)
        controller.set_event_bind(self.HIGH_SCORE, controller.obj_dispatch, HighScoreScreen)
        controller.set_event_bind(self.PLAY_GAME, controller.obj_dispatch, StartButton)
        controller.loop.create_task(self.show())

    async def show(self):
        '''
        Show model view
        TX RGB color data
        
        Update player guess remaining to 0:
            controller.show_player_info()
        
        '''
        await self.controller.ble_tx(self.COLOR_MAP)
        await self.controller.update_gui(self.config, self.COLOR_MAP)
        await self.controller.show_player_info(remaining=0)
        


#-----------------------------------------------------

#    High Score Screen

#-----------------------------------------------------

class HighScoreTools:
    '''
    Constants for HighScoreScreen
    
    COLOR_MAP: Button color matrix
    
    RETURN:  Event - MainMenu or PostGameMenu Dispatch
    
    '''
    COLOR_MAP = 'XXXXXXXXX'
    RETURN = (
        '<q>', '<w>', '<e>',
        '<a>', '<s>', '<d>',
        '<z>', '<x>', '<c>'
    )


class HighScoreScreen(HighScoreTools):
    '''
    HighScoreScreen Model Object
    Dipatch on events to:
    MainMenu or HighScoreScreen
        Depends on game running state
    
    :param controller: Main App controller
    
    '''
    
    def __init__(self, controller):
        
        # set controller and remove event binds
        controller.remove_event_bind()
        self.controller = controller
        
        # set canvas view configs
        settings = (
            ('background', {'fill': 'black'}), 
            ('scores', {'text': '', 'font': controller.set_font(size=30, style='bold italic'),
                                    'fill': color.WHT, 'justify': 'left'})       
        )
        self.config = config.GenericConfig('highscore', 'normal', settings).configs
        
        # if game is running return to PostGameMenu
        if controller.game_running is True:
            controller.set_event_bind(self.RETURN, controller.obj_dispatch, PostGameMenu)
        
        # else return to MainMenu
        else:
            controller.set_event_bind(self.RETURN, controller.obj_dispatch, MainMenu)
        
        # update the highscores and add model to asyncio loop
        self.update_highscores()
        controller.loop.create_task(self.show())

    def update_highscores(self):
        '''
        Get and display highscore data
        
        '''
        scores = ''
        file = open(path.SCOREBOARD, 'r')
        for i, line in enumerate(file):
            scores += str(i) + '.\t' + line.replace(' ', '\t') + '\n'
        self.config['scores']['text'] = 'RANK\tNAME\tSCORE\n\n'
        self.config['scores']['text'] += scores

    async def show(self):
        '''
        Show model view
        TX RGB color data
        
        Hide Player Info:
            controller.clear_player_info()
        
        '''
        await self.controller.ble_tx(self.COLOR_MAP)
        await self.controller.update_gui(self.config, clear=True)
        await self.controller.clear_player_info()
