# Authors: Ellis Hobbby
# Version: 1.0

import asyncio as io
import random
from util.color import DEFAULT
from model.model import Model, KEY_TO_NUM

class TicTacToe(Model):

    SPOT = [
        '<q>', '<w>', '<e>', 
        '<a>', '<s>', '<d>',
        '<z>', '<x>', '<c>'
    ]

    def __init__(self, *args):
        b_font  = Model.font(size= 100) 
        m_font = Model.font(size= 60)
        config = {
            'title': {'text': ''},
            'bg-txt': {'text': 'CHOOSING\n\nSTARTING\n\nPLAYER\n', 
                       'font': m_font, 'justify': 'center'}
        }     
        self.button = []
        for i in range(9):
            config.update({f'txt-{i}': {'text': '', 'font': b_font}})  
            self.button.append(config[f'txt-{i}']) 

        self.title   = config['title']
        self.message = config['bg-txt']

        color = None

        super().__init__(config, color, music=False)

        self.pick_event = {**dict.fromkeys(self.SPOT, self.pick)}

        self.loop.create_task(self.run())


    async def run(self):

        self.count   = 0
        self.turn    = 0
        self.winner  = None
        self.picked  = []
        self.board   = ['-']*9
        self.bot = [i for i in range(9)]

        Model.game_run = True

        Model.player_1.info['symbol'] = 'X'
        Model.player_2.info['symbol'] = 'O'
        Model.computer.info['symbol'] = 'O'

        if Model.multiplayer is True:
            Model.active_player = Model.player_2.info 
            self.update()
        
        else:
            Model.active_player = Model.computer.info 
            self.update()

        await io.sleep(0.01)

        Model.active_player = Model.player_1.info 
        self.update()

        for i in range(5):
            self.message['text'] += '.'     
            await io.sleep(1)
            self.update()

        self.starting_player()
        await io.sleep(3)
        self.message['text'] = ''
        self.color = DEFAULT
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

        Model.highlight = 2

        if (self.turn == 0) and (Model.multiplayer is True): 
            Model.active_player = Model.player_2.info
            self.turn = 1
            self.title['text'] = 'TURN:  PLAYER 2' 
            self.event = self.pick_event

        elif (self.turn == 0) and (Model.multiplayer is False):
            self.turn = 1
            self.title['text'] = 'COMPUTER CHOOSING...' 
            self.event = []
            self.loop.create_task(self.computer())

        else:
            Model.active_player = Model.player_1.info
            Model.highlight = 1
            self.turn = 0
            self.title['text'] = 'TURN:  PLAYER 1' 
            self.event = self.pick_event

        self.update()


    def pick(self, key):

        self.clear_event()
        spot = KEY_TO_NUM[key]

        if spot not in self.picked:
            
            self.picked.append(spot)
            idx = self.bot.index(spot)
            self.bot.pop(idx)
            
            symbol  = Model.active_player['symbol'] 

            p_color = ['R', 'G']
            p_color = p_color[self.turn]

            self.button[spot]['text'] = symbol
            self.board[spot] = symbol
            self.color = self.color[:spot] + p_color + self.color[spot+1:]
            self.count += 1
                
            if self.count >= 5:
                self.check()

            if (self.winner == None) and (self.count != 9):
                self.set_turn()
        
        else:
            self.event = self.pick_event
            self.update()
            
            
    async def computer(self):

        await io.sleep(3)

        if len(self.bot) == 0:
            pick = self.bot[0]
        else:
            pick = random.randrange(0,len(self.bot))

        spot = self.bot.pop(pick)
        self.picked.append(spot)

        self.button[spot]['text'] = 'O'
        self.board[spot] = 'O'
        self.color = self.color[:spot] + 'G' + self.color[spot+1:]
        self.count += 1
            
        if self.count >= 5:
            self.check()

        if (self.winner == None) and (self.count != 9):
            self.set_turn()


    def check(self):

        self.update()

        r1 = [x for x in self.board[0:3:1]]
        r2 = [y for y in self.board[3:6:1]]
        r3 = [z for z in self.board[6:9:1]]

        c1 = [x for x in self.board[0:9:3]]
        c2 = [y for y in self.board[1:9:3]]
        c3 = [z for z in self.board[2:9:3]] 

        for i in range(3):
            if  r1[i] == r2[i] == r3[i] != '-':
                self.winner = r1[i]
                break    
            elif c1[i] == c2[i] == c3[i] != '-':
                self.winner = c1[i]   
                break 
            elif r1[0] == r2[1] == r3[2] != '-':
                self.winner = r1[0]
                break 
            elif r1[2] == r2[1] == r3[0] != '-' :
                self.winner = r1[2]
                break 
        
        if (self.winner) or (self.count == 9):
            self.loop.create_task(self.end())


    async def end(self):

        await io.sleep(1)

        p_win = 'WINNER:\n----------\n\nPLAYER {num}\n\n{name}\n\n----------'

        if self.winner == None:
            self.message['text'] = '----------\n\nDRAW\n\nNO WINNER\n\n----------'

        elif self.winner == 'X':
            Model.player_1.info['score'] += 1
            name = Model.player_1.info['name']
            self.message['text'] = p_win.format(num=1, name=name)

        elif (self.winner == 'O') and (Model.multiplayer == True):
            Model.player_2.info['score'] += 1
            name = Model.player_2.info['name']
            self.message['text'] = p_win.format(num=2, name=name)

        else:
            Model.computer.info['score'] += 1
            self.message['text'] = '----------\n\nCOMPUTER\n\nWINS\n\n----------'

        self.config = {'bg-txt': self.message}
        self.color  = None
        Model.highlight = None
        self.update()
        
        await io.sleep(5)
        self.new_model('post-game')
