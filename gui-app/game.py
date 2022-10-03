# Authors: Ellis Hobbby, Ryan White
# Version: 2.0


import asyncio
import subprocess
import random
import menus
from util import config, path, color


"""---------------------------------------------
    
    IMPORTANT INFO:

    * Must change paths in /util/path.py *
    

---------------------------------------------"""


class GameTools:
    '''
    Constants for PlayGame
    
    PATTERN_DELAY: How long between
                   pattern sequence
                   
    NUM_LOOPS: How many pattern loops
    
    GUESS_INPUT: Event - calls guess_event()
    
    REVEAL_COUNTDOWN_COLOR: Color map for countdown
    
    KEY_TO_NUM: Dict to index event keys
    
    '''
    PATTERN_DELAY = 0.5
    NUM_LOOPS = 3

    GUESS_INPUT = [
        '<q>', '<w>', '<e>', 
        '<a>', '<s>', '<d>',
        '<z>', '<x>', '<c>'
    ]
    REVEAL_COUNTDOWN_COLOR = 'XXXXWXXXX'

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

    


class PlayGame(GameTools):
    
    def __init__(self, controller):
        
        # save controller and remove event binds
        controller.remove_event_bind()
        self.controller = controller
        
        # update controller game running state
        controller.game_running = True
        
        # update canvas view configs
        settings = [('count', {'text': '', 'font': controller.set_font(size=100)})]
        self.config = config.GenericConfig('winning', 'normal', settings).configs
        
        # vars for game strings
        self.pattern_1 = color.DEF_PATTERN
        self.pattern_2 = color.DEF_PATTERN
        self.winning_color = ''
        self.rand_pattern = ''
        
        # vars game mechanics
        self.guess_colors = color.DEF_PATTERN
        self.guess_list = []
        self.score = 0
        self.index = -1
        self.counter = 0
        
        # get colors and update patterns
        self.get_colors()
        self.set_patterns()
        
        # add model to asyncio loop, start running game
        controller.loop.create_task(self.game_run())


    def get_colors(self):
        '''
        Call backend to generate new random pattern
        Read random pattern and correct color from file
        
        '''
        subprocess.run([path.BACKEND_PATH, path.BACKEND_ARG_COLOR])  
        
        pattern_file = open(path.COLOR_PATTERN, 'r')
        correct_file = open(path.CORRECT_COLOR, 'r')

        self.rand_pattern = pattern_file.readline().rstrip('\n')
        self.winning_color = correct_file.readline().rstrip('\n') 

        pattern_file.close()
        correct_file.close()


    def set_patterns(self):
        '''
        Split random pattern
        
        '''
        picker = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        random.shuffle(picker)

        slicer = random.randrange(4,6)

        for i in picker[0:slicer]:
            self.pattern_1 = self.pattern_1[:i] + self.rand_pattern[i] + self.pattern_1[i+1:]
      
        for i in picker[slicer:len(picker)]:
            self.pattern_2 = self.pattern_2[:i] + self.rand_pattern[i] + self.pattern_2[i+1:] 


    async def game_run(self):
        '''
        Loop through patterns
        and show winning color

        '''
        for i in range(self.NUM_LOOPS):
            await self.display_pattern(self.pattern_1)
            await self.display_pattern(self.pattern_2)

        await self.reveal_winning_color()


    async def display_pattern(self, color_string):
        '''
        Show pattern for delay time
        Clear pattern for delay time
        BLE TX color data
        
        '''
        await self.controller.ble_tx(color_string)
        await self.controller.update_gui(None, color_string)
        await asyncio.sleep(self.PATTERN_DELAY)
            
        await self.controller.ble_tx(color.DEF_PATTERN)
        await self.controller.update_gui(None, color.DEF_PATTERN)
        await asyncio.sleep(self.PATTERN_DELAY)  


    async def reveal_winning_color(self):
        '''
        Countdown to show winning color
        Reveal winning color
        Begin guess event
        
        '''
        # update canvas view with countdown color map
        await self.controller.update_gui(None, self.REVEAL_COUNTDOWN_COLOR)
        
        # countdown from 3, display count on cavas
        countdown = 3
        while countdown:
            self.config['count']['text'] = countdown
            await self.controller.update_gui(self.config)
            await asyncio.sleep(2)
            countdown -= 1
        
        # create full size color string from winning_color
        winning_string = ''
        for i in range(len(self.rand_pattern)):
            winning_string += self.winning_color
        
        # show winning color for 5 seconds
        # BLE TX winning color
        # beging guess event
        await self.controller.ble_tx(winning_string)
        await self.controller.update_gui(None, winning_string)
        await asyncio.sleep(5)
        await self.controller.update_gui(None, color.DEF_PATTERN) 
        self.set_guess_event()


    def set_guess_event(self):
        '''
        set event bind to guess_event()
        
        '''
        self.controller.set_event_bind(self.GUESS_INPUT, self.guess_event)
       
       
    async def guess_event(self, key):
        '''
        Check user input against the random pattern
        If input index color matches winning color
        update score
        
        :param key: event key press
        
        '''
        
        # set key to index value
        guess = self.KEY_TO_NUM[key]
        
        # if the guess has not been tried update
        if guess not in self.guess_list:
            
            # add guess to list ref
            self.guess_list.append(guess)
            
            # update guess remaining and display
            guess_amt = (3 - len(self.guess_list))
            await self.controller.show_player_info(remaining=guess_amt)
            
            # retrieve the guessed color
            color = self.rand_pattern[guess]
            self.guess_colors = self.guess_colors[:guess] + color + self.guess_colors[guess+1:]
            
            # display the guessed color and BLE TX
            await self.controller.ble_tx(self.guess_colors)
            await self.controller.update_gui(None, self.guess_colors)
            
            # if guessed color equals winning color update player total
            if color == self.winning_color:
                self.score += 1
                self.controller.total += 1
                await self.controller.show_player_info(remaining=guess_amt)
        
        # if three guesses made, update player round score
        # dispatch PostGameMenu
        if len(self.guess_list) == 3:
            self.controller.score = self.score
            await asyncio.sleep(1)
            await self.controller.obj_dispatch(menus.PostGameMenu)
    