# Authors: Ellis Hobbby, Ryan White
# Version: 3.0

import asyncio as io
import subprocess
import random

from model.model import Model, KEY_TO_NUM
from util.color  import DEFAULT
from util.path   import *


"""---------------------------------------------
    
    IMPORTANT INFO:

    * Must change paths in /util/path.py *
    

---------------------------------------------"""
class MemoryGame(Model):

    DELAY = 1
    LOOPS = 3

    GUESS = [
        '<q>', '<w>', '<e>', 
        '<a>', '<s>', '<d>',
        '<z>', '<x>', '<c>'
    ]

    def __init__(self, *args):
        font   = Model.font(size= 100)
        m_font = Model.font(size= 60)
        config = {
            'txt-4': {'text': '', 'font': font},
            'title': {'text': ''},
            'bg-txt': {'text': 'GET READY\n',
                        'font': m_font, 'justify': 'center'}
        }
        self.title = config['title']
        self.count = config['txt-4']
        self.message = config['bg-txt']

        color = None
        
        self.guess_event = {**dict.fromkeys(self.GUESS, self.guess)}

        super().__init__(config, color, music=False)

        # update controller game running state
        Model.game_run = True

        self.player = Model.active_player
        self.player['guess'] = 3

        # vars game mechanics
        self.guess_color = DEFAULT
        self.guess_list  = []

        # add model to asyncio loop, start running game
        self.loop.create_task(self.run())


    def get_colors(self):
        '''
        Call backend to generate new random pattern
        Read random pattern and correct color from file
        
        '''
        subprocess.run([BACKEND_PATH, BACKEND_ARG_COLOR, MAIN_DIR])  
        
        pattern_file = open(COLOR_PATTERN, 'r')
        correct_file = open(CORRECT_COLOR, 'r')

        self.full = pattern_file.readline().rstrip('\n')
        self.win  = correct_file.readline().rstrip('\n')
        
        self.full = self.full[:9]

        pattern_file.close()
        correct_file.close()

    async def run(self):
        '''
        Loop through patterns
        and show winning color

        '''
        for i in range(5):
            self.message['text'] += '.'
            await io.sleep(1)
            self.update()
            
        self.message['text'] = ''
        self.title['text'] = 'WATCH THE PATTERNS'
        self.color = DEFAULT
        self.update()
        await io.sleep(3)
           
        
         # get colors and update patterns
        self.get_colors()
        self.set_patterns()
        
        self.title['text'] = 'WATCH THE PATTERNS' 
        for i in range(self.LOOPS):
            await self.display(Model.pattern[0])
            await self.display(Model.pattern[1])

        await self.reveal()

        self.event = self.guess_event
        self.update()


    def set_patterns(self):
        '''
        Split random pattern
        
        '''
        picker = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        random.shuffle(picker)

        slicer  = random.randrange(4,6)

        temp = DEFAULT
        for i in picker[0:slicer]:
            temp = temp[:i] + self.full[i] + temp[i+1:]
        Model.pattern[0] = temp

        temp = DEFAULT
        for i in picker[slicer:len(picker)]:
            temp = temp[:i] + self.full[i] + temp[i+1:]
        Model.pattern[1] = temp


    async def display(self, pattern):
        '''
        Show pattern for delay time
        Clear pattern for delay time
        BLE TX color data
        '''
        self.color = pattern
        self.update()
        await io.sleep(self.DELAY)  
        
        self.color = DEFAULT
        self.update()
        await io.sleep(self.DELAY)  


    async def reveal(self):
        '''
        Countdown to show winning color
        Reveal winning color
        Begin guess event
        
        '''
        # update canvas view with countdown color map
        self.title['text'] = 'GET READY'
        
        # countdown from 3, display count on cavas
        for counter in range(3, 0, -1):
            self.count['text'] = counter
            self.color = 'XXXXWXXXX'
            self.update()
            await io.sleep(2)

        # create full size color string from winning_color
        reveal = ''
        for i in range(len(self.full)): reveal += self.win
        self.color = reveal
        
        # show winning color for 5 seconds
        # BLE TX winning color
        # beging guess event
        self.count['text'] = ''
        self.title['text'] = 'FIND THIS COLOR'
        self.update()
        await io.sleep(5)
        
        self.title['text'] = ''
        self.color = DEFAULT
        self.update()
       
       
    def guess(self, key):
        '''
        Check user input against the random pattern
        If input index color matches winning color
        update score
        
        :param key: event key press
        
        '''

        self.clear_event()
        
        # set key to index value
        guess = KEY_TO_NUM[key]
        
        # if the guess has not been tried update
        if guess not in self.guess_list:
            
            # add guess to list ref
            self.guess_list.append(guess)
            
            # update guess remaining and display
            self.player['guess'] = (3 - len(self.guess_list))
            
            # retrieve the guessed color
            color = self.full[guess]
            self.guess_color = self.guess_color[:guess] + color + self.guess_color[guess+1:]    
            
            # if guessed color equals winning color update player total
            if color == self.win:
                self.player['score'] += 1
            
            self.color = self.guess_color
            self.update()
        
        # if three guesses made, update player round score
        # dispatch PostGameMenu
        if len(self.guess_list) == 3:
            self.loop.create_task(self.end())

        else:
            self.event = self.guess_event
            self.update()


        
    
    async def end(self):
        
        await io.sleep(1)

        if Model.multiplayer is True:
            if self.player['player'] == 1:
                Model.player_1.info = self.player
                Model.active_player = Model.player_2.info
                self.new_model('start-button')
            else:
                Model.player_2.info = self.player
                Model.active_player = Model.player_1.info
                self.new_model('post-game')
        else: 
            self.new_model('post-game')




