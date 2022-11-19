

INFO = '[ {p} ]\n-----------\nNAME: {n}\n\nSCORE: {s}\n\n\n'
GUESS = 'GUESS: {}\n'
SYMBOL = 'SYMBOL: {}\n'
TOTAL = 'TOTAL: {}\n'




class DynamicPlayerDict(dict):
    def __getitem__(self, key):
        
        if  key == 'INFO':
            return INFO.format( p=self['tag'],
                                n=self['name'],
                                s=self['score'])
        elif key == 'GUESS':
            return self['INFO'] + GUESS.format(self['guess'])
       
        elif key == 'SYMBOL':
            return self['INFO'] + SYMBOL.format(self['symbol'])
        
        elif key == 'TOTAL':
            return self['INFO'] + TOTAL.format(self['total'])
        
        elif key == 'TEXT':
            
            config = {'tagOrId': self['tagtxt'], 'state': 'normal'}
            
            if self['game'] == None:
                config['text'] = self['INFO']
        
            elif self['game'] == 'tic-tac-toe':
                config['text'] = self['SYMBOL']

            elif self['game'] == 'memory':
                config['text'] = self['GUESS']

            elif self['game'] == 'pig-dice':
                config['text'] = self['TOTAL']

            return config

        elif key == 'IMAGE':
            return {'tagOrId': self['tagimg'], 'image': self['avatar'], 'state': 'normal'}

        elif key == 'HIGHLIGHT':
            return {'tagOrId': self['tagrec'], 'state': 'normal'}
            
        
        return dict.__getitem__(self, key)





class Player(DynamicPlayerDict):
    def __init__(self, player, top, bot, rec):
        if player: 
            self.tag  = f'PLAYER {player}'
            self.name = ''
        else:
            self.tag  = 'COMPUTER'
            self.name = 'BOT'
        self.num    = player
        self.tktop  = top   
        self.tkbot  = bot 
        self.tkrec  = rec 
        self.reset()

    def reset(self):
        self.info  = DynamicPlayerDict(
            player = self.num,
            tag    = self.tag,
            name   = self.name,
            score  = 0,
            total  = 0,
            avatar = None,
            avindex = None,
            
            guess  = 0,
            symbol = None,
            game   = None, 

            tagtxt = self.tktop,
            tagimg = self.tkbot,
            tagrec = self.tkrec
        )
