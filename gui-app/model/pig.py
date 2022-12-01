# Authors: Ellis Hobbby
# Version: 1.0

import asyncio as io
import random
from util.color import DEFAULT
from model.model import Model, KEY_TO_NUM

ONE   = 'xxxxDxxxx'
TWO   = 'DxxxxxxxD'
THREE = 'xxDxDxDxx'
FOUR  = 'DxDxxxDxD'
FIVE  = 'DxDxDxDxD'
SIX   = 'DxDDxDDxD'

DICE  = [ONE, TWO, THREE, FOUR, FIVE, SIX]


class PigDice(Model):

    R_COLOR = 'xxxxGxxxx'

    def __init__(self, *args):
    
        m_font = Model.font(size=60)
        config = {
            'title': {'text': ''},
            'txt-4': {'text': ''},
            'bg-txt': {'text': 'CHOOSING\n\nSTARTING\n\nPLAYER\n', 
                       'font': m_font, 'justify': 'center'}
        }     
        self.title   = config['title']
        self.press   = config['txt-4']
        self.message = config['bg-txt']
        
        color = None

        super().__init__(config, color, music=False)

        ROLL = ['<s>']
        self.roll_event = {**dict.fromkeys(ROLL, self.roll)}

        self.loop.create_task(self.run())

    
    async def run(self):

        Model.player_1.info['total'] = 0
        Model.player_2.info['total'] = 0
        Model.computer.info['total'] = 0

        if Model.multiplayer is True:
            Model.active_player = Model.player_2.info 
            self.update()
        
        else:
            Model.active_player = Model.computer.info 
            self.update()

        await io.sleep(0.1)

        for i in range(5):
            self.message['text'] += '.'     
            await io.sleep(1)
            self.update()

        
        self.starting_player()
        await io.sleep(3)
        self.message['text'] = ''

        self.press['text'] = 'ROLL\nDICE'
        self.color = self.R_COLOR
        
        self.set_turn()


    def starting_player(self):
        
        self.turn = random.randrange(0,2)

        Model.highlight = 2
        
        if (self.turn == 0) and (Model.multiplayer is True):
            name = Model.player_2.info['name']
            self.message['text'] = f'----------\n\nPLAYER 2\n\n{name}\n\nGOES FIRST\n\n----------'
            
        elif (self.turn == 0) and (Model.multiplayer is False):
            self.message['text'] = '----------\n\nCOMPUTER\n\nGOES FIRST\n\n----------'
        
        else:
            name = Model.player_1.info['name']
            Model.highlight = 1
            self.message['text'] = f'----------\n\nPLAYER 1\n\n{name}\n\nGOES FIRST\n\n----------'

        self.update()


    def set_turn(self):

        self.press['text'] = 'ROLL\nDICE'
        self.color = self.R_COLOR

        Model.highlight = 2

        if (self.turn == 0) and (Model.multiplayer is True): 
            Model.active_player = Model.player_2.info
            self.turn = 1
            self.title['text'] = 'ROLL:  PLAYER 2' 
            self.event = self.roll_event

        elif (self.turn == 0) and (Model.multiplayer is False):
            Model.active_player = Model.computer.info
            self.turn = 1
            self.title['text'] = 'COMPUTER ROLLING...' 
            self.event = []
            self.loop.create_task(self.computer())

        else:
            Model.active_player = Model.player_1.info
            Model.highlight = 1
            self.turn = 0
            self.title['text'] = 'ROLL:  PLAYER 1' 
            self.event = self.roll_event

        self.update()    


    async def _roll(self):
        
        self.press['text']   = ''
        
        last = idx = 0

        for i in range(4):

            self.color = DEFAULT
            self.update()
            await io.sleep(0.5)

            while idx == last:
                idx = random.randrange(0,6)
            
            last = idx
            die = DICE[idx]
            self.color = die.replace('D', 'R')
            self.update()
            await io.sleep(0.5)

        Model.active_player['total'] += (idx+1)
        self.update()
        
        await io.sleep(1)

        
        if Model.active_player['total'] >= 100:
            self.loop.create_task(self.end())

        else:
            
            if idx == 0:
                self.message['text'] = 'UH-OH YOU\n\nROLLED A 1\n\nNEXT PLAYER' 
                self.press['text']   = ''
                self.color = None
                self.update()
                await io.sleep(2)
                self.message['text'] = '' 
                self.set_turn()

            elif (self.turn == 1) and (Model.multiplayer is False):
                self.press['text'] = 'ROLL\nDICE'
                self.color = self.R_COLOR
                self.loop.create_task(self.computer())

            else:
                self.press['text'] = 'ROLL\nDICE'
                self.color = self.R_COLOR
                self.event = self.roll_event
                self.update()

             
            

    
    def roll(self, key): 

        self.clear_event()
        self.event = []
        self.loop.create_task(self._roll())


    async def computer(self):

        self.update()
        await io.sleep(1)
        self.loop.create_task(self._roll())



    async def end(self):

        self.title['text'] = ''
        self.press['text'] = ''
        self.color = None
        Model.highlight = None

        if (self.turn == 1) and (Model.multiplayer is False):
            self.message['text'] = '----------\n\nCOMPUTER\n\nWINS\n\n----------'

        else:
            Model.active_player['score'] += 1
            name = Model.active_player['name']
            num  = Model.active_player['player']
            self.message['text'] = f'WINNER:\n----------\n\nPLAYER {num}\n\n{name}\n\n----------'

        self.update()
        
        await io.sleep(5)
        self.new_model('post-game')
    




        
        


        
