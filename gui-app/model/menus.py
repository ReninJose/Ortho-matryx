# Authors: Ellis Hobbby, Ryan White
# Version: 2.0

import asyncio as io
import subprocess

from model.model import Model, KEY_TO_NUM, LETTERS
from util.path   import *



"""---------------------------------------------
    
    IMPORTANT INFO:

    * Must change paths in /util/path.py *
    
---------------------------------------------"""



#-----------------------------------------------------

#    Title Screen

#-----------------------------------------------------
class TitleScreen(Model):
    '''
    TitleScreen Model Object
    Will be shown when BLE peripheral
    not connected and game is idle
    
    Dispatches MainMenu on button event
    
    :param controller: Main App controller
    
    '''   
    def __init__(self, *args):
        config = {
            'txt-3': {'text': 'ORTHO'},
            'txt-4': {'text': 'MATRYX'},
            'txt-7': {'text': 'GAME'},
            'title': {'text': 'TITLE SCREEN'}
        }
        color = 'RGBWWRGWB'

        menu = (
            '<q>', '<w>', '<e>',
            '<a>', '<s>', '<d>',
            '<z>', '<x>', '<c>'
        )
        event = {**dict.fromkeys(menu, Model.sub['main-menu'])}
        event = None
     
        

        Model.reset_game_data()

        super().__init__(config, color, event, music=False)
       
#-----------------------------------------------------

#    Menu Screen

#-----------------------------------------------------
class MainMenu(Model):
    '''
    MainMenu Model Object
    Dipatch on events to:
    quickplay, avatar menu, exit, high scores
    
    :param controller: Main App controller
    
    ''' 
    def __init__(self, *args):
        config = {
            'txt-0': {'text': 'QUICK\nPLAY'},
            'txt-2': {'text': 'SINGLE\nPLAYER'},
            'txt-4': {'text': 'MULTI\nPLAYER'},
            'txt-6': {'text': 'EXIT\nGAME'},
            'txt-8': {'text': 'HIGH\nSCORES'},
            'title': {'text': 'MAIN MENU'}
        }
        color = 'GXGXBXRXW'

        QUICK = ['<q>']
        MODE  = ['<e>', '<s>']
        QUIT  = ['<z>']
        HIGH  = ['<c>']
        event = {
            **dict.fromkeys(QUICK, Model.sub['start-button']),
            **dict.fromkeys(MODE, Model.sub['avatar-menu']),
            **dict.fromkeys(QUIT, Model.ble_disconnect),
            **dict.fromkeys(HIGH, Model.sub['high-score'])
        }
        
        Model.reset_game_data()

        super().__init__(config, color, event, music=True)
        


#-----------------------------------------------------

#    Game Selection Screen

#-----------------------------------------------------
class GameSelect(Model):
    '''
    GameSelect Model Object
    Dipatch on events to:
    game_select(), two_player(), MainMenu, AvatarMenu
    
    :param controller: Main App controller
    
    '''
    
    CONFIRM = ['<c>']

    def __init__(self, *args):
        config = {
            'txt-0': {'text': 'TIC\nTAC\nTOE'},
            'txt-1': {'text': 'MEMORY\nGAME'},
            'txt-2': {'text': 'PIG\nDICE\nGAME'},
            'txt-6': {'text': 'EXIT'},
            'txt-8': {'text': ''},
            'title': {'text': 'SELECT A GAME'}
        }
        self.title   = config['title']
        self.confirm = config['txt-8']

        color = 'BBBXXXRXX'

        SELECT  = ['<q>', '<w>', '<e>']
        MENU    = ['<z>']
        event = {
            **dict.fromkeys(SELECT, self.select),
            **dict.fromkeys(MENU, Model.sub['main-menu'])
        }

        super().__init__(config, color, event)

        
         
    
    def select(self, key):

        # confirm is now available
        self.confirm['text'] = 'CONFIRM'

        # translate key to index value
        select = KEY_TO_NUM[key]

        if select == 0:
            Model.game_type = 'tic-tac-toe'
            self.title['text']  = 'TIC TAC TOE'

        elif select == 1:
            Model.game_type = 'memory'
            self.title['text']  = 'MATRIX MEMORY GAME'

        elif select == 2:
            Model.game_type = 'pig-dice'
            self.title['text']  = 'PIG DICE GAME'


        # update the color map to highlight selection
        COLOR = 'BBBXXXRXG'
        self.color = COLOR[:select] + 'W' + COLOR[select+1:]
        
        # enable confirm event to be called - will dispatch AvartarMenu
        event = {**dict.fromkeys(self.CONFIRM, Model.sub['start-button'])}
        self.event.update(event)
        
        # update BLE RGB and canvas view
        self.update()



#-----------------------------------------------------

#    Avatar Screen

#-----------------------------------------------------
class AvatarMenu(Model):
    '''
    AvatarMenu Model Object
    Dipatch on events to:
    avatarselection(), MainMenu, PlayerName
    
    :param controller: Main App controller
    
    '''
    NAME = ['<c>']
    
    def __init__(self, *args):
        
        # if we have reached here,
        # the game is not in quickplay
        Model.quickplay = False
        
        if args:
            if args[0] == 's':
                Model.multiplayer = True

        print(Model.multiplayer)
            
        config = {
            'img-0': {}, 'img-1': {}, 'img-2': {},
            'img-3': {}, 'img-4': {}, 'img-5': {},
            'txt-6': {'text': 'EXIT'},
            'txt-8': {'text': ''},
            'title': {'text': self.title()}
        }
        self.enter = config['txt-8']

        color = 'BBBBBBRXX'

        SELECT  = ['<q>', '<w>', '<e>', '<a>', '<s>', '<d>']
        MENU    = ['<z>']
        event = {
            **dict.fromkeys(MENU, Model.sub['main-menu']),
            **dict.fromkeys(SELECT, self.select)
        }

        Model.game_run = True

        super().__init__(config, color, event)


    def title(self):
        
        number = Model.highlight = Model.active_player['player']

        if Model.multiplayer is True:
            return (f'PLAYER {number}:  -  SELECT AN AVATAR')  
        else:
            return ('SELECT AN AVATAR')

        

    def select(self, key):
        '''
        Each time a player presses an avatar spot,
        its button space is highlighted and its
        index value is updated in the controller.
        
        PlayerName Event is now dispatched
        
        :parap key: the key pressed during event
                    translated to index value
                    using KEY_TO_NUM dict
        
        '''
        # translate key to index value
        select = KEY_TO_NUM[key]
        
        Model.player_avatar(select)

        # update the color map to highlight selection
        COLOR = 'BBBBBBRXG'
        self.color = COLOR[:select] + 'W' + COLOR[select+1:]

        self.enter['text'] = 'ENTER\nNAME'
        
        # enable PlayName event to be called
        event = {**dict.fromkeys(self.NAME, Model.sub['player-name'])}
        self.event.update(event)
        self.update()
        
        

#-----------------------------------------------------

#    Player Name Enter Screen

#-----------------------------------------------------
class PlayerName(Model):
    '''
    PlayerName Model Object
    Dipatch on events to:
    enter_name()
    
    :param controller: Main App controller
    
    '''
    
    # used for tracking player name selection
    index = len(LETTERS) - 1
    count = 0

    def __init__(self, *args):
        letter = Model.font(size=100)
        arrow  = Model.font(size=60)
        config = {
            'txt-0': {'text': '', 'font': letter},
            'txt-1': {'text': '', 'font': letter},
            'txt-2': {'text': '', 'font': letter},
            'txt-6': {'text': '<<<', 'font': arrow},
            'txt-7': {'text': 'ENTER'},
            'txt-8': {'text': '>>>', 'font': arrow},
            'title': {'text': self.title()}
        }
        color = 'WWWXXXRGB'

        NAME  = ['<z>', '<x>', '<c>']
        event = {**dict.fromkeys(NAME, self.enter)}

        super().__init__(config, color, event)


    def title(self):

        if Model.multiplayer is True:
            number = Model.active_player['player']
            return (f'PLAYER {number}  -  ENTER YOUR NAME') 
        else:
            return ('ENTER YOUR NAME')  

       
    def enter(self, key):
        '''
        Called during player name sequence
        
        :param key: the key pressed during event
        
        '''   
        # z moves backwards through the letters
        # decrements the index and wraps back
        if key == 'z':
            self.index -= 1
            if self.index == -1:
                self.index = len(LETTERS) - 1
        
        # z moves forwards through the letters
        # increments the index and wraps back
        if key == 'c':
            self.index += 1
            if self.index == len(LETTERS):
                self.index = 0
                
        # uses the current index to display letter
        select = LETTERS[self.index] 
        self.config[f'txt-{self.count}']['text'] = select

        # x makes a letter selection
        # reset index, inc counter, add to name
        if key == 'x':
            self.index = -1
            self.count += 1
            Model.active_player['name'] += select
        
        self.update()

        # if player has selected three letters
        # add player name to canvas panel view
        # dispatch StartButton
        if self.count == 3:
            self.clear_event()
            self.ctrl.loop.create_task(self.done())

        
    async def done(self):

        await io.sleep(0.1)

        if Model.multiplayer is True:

            if Model.active_player['player'] == 1:
                Model.active_player = Model.player_2.info 
                Model.new_model('avatar-menu')
            else:
                Model.active_player = Model.player_1.info
                Model.highlight = None
                Model.new_model('game-select')
        else:
            Model.highlight = None
            Model.new_model('game-select')
            



#-----------------------------------------------------

#    Start Button Screen

#-----------------------------------------------------
class StartButton(Model):
    '''
    StartButton Model Object
    Dipatch on events to:
    PlayGame
    
    :param controller: Main App controller
    
    '''
    def __init__(self, *args):
        
        START = ['<s>']
        EXIT  = ['<q>']
        
        if Model.quickplay:
            config = {
                'txt-0': {'text': 'EXIT'},
                'txt-4': {'text': 'START\nGAME'},
                    
                'title': {'text': self.title()}
            }
            color = 'RXXXGXXXX'
            
            event = {
                **dict.fromkeys(EXIT, Model.sub['main-menu']),
                **dict.fromkeys(START, Model.new_game)
            }
            
            Model.game_type = 'memory'
     
            
        else:
            config = {
                'txt-0': {'text': 'EXIT'},
                'txt-2': {'text': 'CHANGE\nGAME'},
                'txt-4': {'text': 'START\nGAME'},
                    
                'title': {'text': self.title()}
            }
            color = 'RXBXGXXXX'
            NEW   = ['<e>']
            
            event = {
                **dict.fromkeys(EXIT, Model.sub['main-menu']),
                **dict.fromkeys(NEW, Model.sub['game-select']),
                **dict.fromkeys(START, Model.new_game)
            }

            Model.player_1.info['game'] = Model.game_type
            Model.player_2.info['game'] = Model.game_type 
            Model.computer.info['game'] = Model.game_type
            
            
        
        super().__init__(config, color, event)

         

    def title(self):

        # if in quickplay reset player score to 0
        if Model.quickplay is True:
            Model.active_player['score'] = 0

        if (Model.multiplayer is True) and (Model.game_type == 'memory'):
            number = Model.active_player['player']
            return (f'PLAYER {number}:  -  PRESS TO START')
        else:
            
            Model.active_player = Model.computer.info 
            Model.player_avatar(5)
            
            Model.active_player = Model.player_1.info 
            return ('PRESS TO START') 

        
       

#-----------------------------------------------------

#    Post Game Menu Screen

#-----------------------------------------------------
class PostGameMenu(Model):
    '''
    PostGameMenu Model Object
    Dipatch on events to:
    MainMenu, HighScoreScreen, PlayGame
    
    :param controller: Main App controller
    
    '''  
    def __init__(self, *args):
        
        Model.game_run = True
        Model.highlight = None

        font  = Model.font(size=60)
        config = {
            'txt-0': {'text': ''},
            'txt-1': {'text': '', 'font': font},
            'txt-4': {'text': ''},
            'txt-5': {'text': '', 'font': font},
            'txt-6': {'text': 'MAIN\nMENU'},
            'txt-7': {'text': 'HIGH\nSCORES'},
            'txt-8': {'text': 'PLAY\nAGAIN'},
            'title': {'text': ''},
        }
        label_1  = config['txt-0']
        score_1 = config['txt-1']
        label_2  = config['txt-4']
        score_2 = config['txt-5']

        color = 'WWXXXXRBG'

        MENU   = ['<z>']
        HIGH   = ['<x>']
        PLAY   = ['<c>']
        
        event = {
            **dict.fromkeys(MENU, Model.sub['main-menu']),
            **dict.fromkeys(HIGH, Model.sub['high-score']),
            **dict.fromkeys(PLAY, Model.sub['start-button'])
        }
       
        # if not in quickplay, show running total
        # and write to score board
        score = Model.player_1.info['score']
        label_1['text'] = 'ROUND\nSCORE'
        score_1['text'] = score

        if Model.quickplay is False:
            name   = Model.player_1.info['name']
            score  = Model.player_1.info['score']
            avatar = Model.player_1.info['avindex']
            label_1['text'] = f'{name}\nSCORE'
            score_1['text'] = score
            self.write_score(name, score, avatar)
                
            # call backend: write player total to score board
            if Model.multiplayer is True:
                color = 'WWXXWWRBG'
                name  = Model.player_2.info['name']
                score = Model.player_2.info['score']
                avatar = Model.player_2.info['avindex']
                label_2['text'] = f'{name}\nSCORE'
                score_2['text'] = score
                self.write_score(name, score, avatar)
        

        super().__init__(config, color, event, True)

        if Model.multiplayer == True:
            self.loop.create_task(self.player_info())

    

    def write_score(self, name, score, avatar):
        subprocess.run([ BACKEND_PATH, 
                         BACKEND_ARG_SCOREBOARD, MAIN_DIR,
                         name, str(score), str(avatar) ])    


    async def player_info(self):
        
        Model.active_player = Model.player_1.info
        self.update()
        await io.sleep(0.01)
        
        Model.active_player = Model.player_2.info
        self.update()
 




#-----------------------------------------------------

#    High Score Screen

#-----------------------------------------------------
class HighScoreScreen(Model):
    '''
    HighScoreScreen Model Object
    Dipatch on events to:
    MainMenu or HighScoreScreen
        Depends on game running state
    
    :param controller: Main App controller
    
    '''
    def __init__(self, *args):
        
        self.scoreboard = self.highscores()

        self.page  = [(0,3), (3,6), (6,9)]
        self.p_idx = 0
        
        config = self.set_board(self.page[self.p_idx])

        color = None

        self.KEYS = [
            '<q>', '<w>', '<e>',
            '<a>', '<s>', '<d>',
            '<z>', '<x>', '<c>'
        ]
        event = {**dict.fromkeys(self.KEYS, self.next_page)}

        Model.game_run = False

        super().__init__(config, color, event)


    def highscores(self):
        '''
        Get and display highscore data
        
        '''
        with open(SCOREBOARD, 'r') as file: 
            data = [line.split() for line in file]    
        return data


    def set_board(self, page):

        start, stop = page

        self.p_idx += 1

        temp = {'sb-grid': {'fill': 'black'}}

        for i in range(4):
            temp.update({f'sb-label-{i}' : {'fill': 'white'}})

        for i in range(start, stop, 1):

            info   = self.scoreboard[i]
            name   = info[0]
            score  = info[1]
            avatar = Model.scoreboard_avatar(int(info[2]))

            temp.update({f'sb-rank-{i}'  : {'fill' : 'white'}})
            temp.update({f'sb-name-{i}'  : {'text' : name}})
            temp.update({f'sb-score-{i}' : {'text' : score}})
            temp.update({f'sb-avatar-{i}': {'image': avatar}})

        return temp
        

    def next_page(self, key):

        self.config = {}
        self.config = self.set_board(self.page[self.p_idx])

        if self.p_idx == 3:
            
            self.event = []

            # if game is running return to PostGameMenu
            if Model.game_type != None:    
                self.event = {**dict.fromkeys(self.KEYS, Model.sub['post-game'])}

            # else return to MainMenu
            else:
                self.event = {**dict.fromkeys(self.KEYS, Model.sub['main-menu'])}

        self.update()



    
