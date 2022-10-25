# Authors: Ellis Hobbby, Ryan White
# Version: 2.0


class GenericConfig:
    '''
    Creates dicts for canvas config control
    Uses tags to ref canvas items see tags.py
    
    '''
    def __init__(self, main_tag, state, settings):
        self.generic = {'tagOrId': main_tag, 'state': state}
        self.name = main_tag
        self.settings = settings
        self.configs = {}
        self.create()

    def create(self):
        '''
        updates configs dict
        
        '''
        for i in range(len(self.settings)):
            subtag, kwargs = self.settings[i]
            temp = dict(self.generic)
            temp['tagOrId'] += ' ' + subtag
            temp.update(kwargs)
            self.configs.update({subtag: temp})
    
    
    
