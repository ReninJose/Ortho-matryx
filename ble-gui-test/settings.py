import colors

class GenericConfig:
    def __init__(self, main_tag, state):
        self.generic = {'tagOrId': main_tag, 'state': state}
        self.configs = {}
        self.name = main_tag

    def create(self, key, typ, sub_tag, prop):
        temp = dict(self.generic)
        temp['tagOrId'] += ' ' + sub_tag
        temp.update({typ: prop})
        self.configs.update({key: temp})



class Clear(GenericConfig):
    def __init__(self, main_tag='clear', state='hidden'):
        super().__init__(main_tag, state)
        self.settings = [
            ('fill','button',None),
            ('fill','background',None), 
            ('text','text',None), 
            ('image','image',None)  
        ]



class Title(GenericConfig):
    def __init__(self, main_tag='title', state='normal'):
        super().__init__(main_tag, state)
        self.settings = [
            ('text','ortho','ORTHO'), 
            ('text','matryx','MATRYX'), 
            ('text','game','GAME')  
        ]



class Menu(GenericConfig):
    def __init__(self, main_tag='menu', state='normal'):
        super().__init__(main_tag, state)
        self.settings = [
            ('text','avatar','AVATAR\nSELECT'), 
            ('text','play','QUICK\nPLAY')              
        ]



class Avatar(GenericConfig):
    def __init__(self, main_tag='avatar', state='normal'):
        super().__init__(main_tag, state)
        self.settings = [
            ('text','back','MAIN\nMENU'), 
            ('text','play','START\nGAME')   
        ]



class HighScore(GenericConfig):
    def __init__(self, main_tag='highscore', state='normal'):
        super().__init__(main_tag, state)
        self.settings = [
            ('fill', 'background', colors.WHT), 
            ('text','scores','')   
        ]
