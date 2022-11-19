# Authors: Ellis Hobbby, Ryan White
# Version: 2.0


class GenericConfig:
    
    def __init__(self, controller):
        self.view       = {}
        self.reset      = {}
        self.player     = {}
        self.controller = controller
        self.background()
        self.scoreboard()
        self.buttons()
        self.title()
        self.side()

    def background(self):
        
        font = self.controller.set_font(style='italic')
        
        bg   = {'bg': {'state': 'hidden',
                       'fill' : 'black',
                       'tags' : 'bg'}}
        
        txt  = {'bg-txt': {'state': 'hidden',
                           'font' : font,
                           'fill' :'white',
                           'tags' : 'bg-txt'}}
        
        img  = {'bg-img': {'state': 'hidden',
                           'image': None,
                           'tags' : 'bg-img'}}
        
        self.view.update(bg)  ;  self.reset.update(bg)
        self.view.update(txt) ;  self.reset.update(txt)
        self.view.update(img) ;  self.reset.update(img)

    def scoreboard(self):
        
        font = self.controller.set_font(size=40, style='bold italic')

        label_txt = ['RANK', 'NAME', 'SCORE', 'AVATAR']
        
        for i in range(4):
            _label = f'sb-label-{i}'
            label  = {_label: {'state'  : 'hidden',
                               'text'   : label_txt[i],
                               'font'   : font,
                               'fill'   : 'white',
                               'justify': 'center',
                               'tags'   : _label}} 
            
            self.view.update(label)  ;  self.reset.update(label)
       
        for i in range(9):
            _rank    = f'sb-rank-{i}'
            _name    = f'sb-name-{i}'
            _score   = f'sb-score-{i}'
            _avatar  = f'sb-avatar-{i}'

            rank = {_rank: {'state'   : 'hidden',
                            'text'   : str(i+1),
                            'font'   : font,
                            'fill'   : 'white',
                            'justify': 'center',
                            'tags'   : _rank}}

            name = {_name: {'state'  : 'hidden',
                            'text'   : '',
                            'font'   : font,
                            'fill'   : 'white',
                            'justify': 'center',
                            'tags'   : _name}}  

            score = {_score: {'state'  : 'hidden',
                              'text'   : '',
                              'font'   : font,
                              'fill'   : 'white',
                              'justify': 'center',
                              'tags'   : _score}}

            avatar  = {_avatar: {'state': 'hidden',
                                 'image': None,
                                 'tags' : _avatar}}
            
            self.view.update(rank)   ;  self.reset.update(rank)
            self.view.update(name)   ;  self.reset.update(name)
            self.view.update(score)  ;  self.reset.update(score)
            self.view.update(avatar) ;  self.reset.update(avatar)

        grid  = {'sb-grid': {'state'  : 'hidden',
                             'fill'   : 'black',
                             'outline': 'white',
                             'width'  : 5,
                             'tags'   : 'sb-grid'}}

        self.view.update(grid)   ;  self.reset.update(grid)
        


    def buttons(self):
        
        font = self.controller.set_font()
    
        for i in range(9):
            
            _btn = f'btn-{i}'
            _txt = f'txt-{i}'
            _img = f'img-{i}'
            
            btn  = {_btn: {'state'  : 'hidden',
                           'fill'   : 'black',
                           'outline': 'black',
                           'width'  : 10,
                           'tags'   : _btn}}
            
            txt  = {_txt: {'state'  : 'hidden',
                           'text'   : '',
                           'font'   : font,
                           'fill'   : 'black',
                           'justify': 'center',
                           'tags'   : _txt}}
            
            img  = {_img: {'state': 'hidden',
                           'tags' : _img}}
            
            self.view.update(btn) ;  self.reset.update(btn)
            self.view.update(txt) ;  self.reset.update(txt)
            self.view.update(img) ;  self.reset.update(img)
 
 
    def title(self):
        
        font  = self.controller.set_font(size=25)
  
        title = {'title': {'state': 'hidden',
                           'fill' : 'white',
                           'font' : font,
                           'tags' : 'title'}}
        
        self.view.update(title) ;  self.reset.update(title)


    def side(self):
        
        font  = self.controller.set_font(size=18)

        rec_1 = {'player-1-rec': {'state'  : 'hidden',
                                  'fill'   : 'black',
                                  'outline': 'white',
                                  'width'  : 5,
                                  'tags'   : ('player-rec-clear', 'player-1-rec')}}
        
        txt_1 = {'player-1-txt': {'state' : 'hidden',
                                  'fill'  : 'white',
                                  'font'  : font,
                                  'anchor': 'nw',
                                  'tags'  : ('player-txt-clear', 'player-1-txt')}}
        
        img_1 = {'player-1-img': {'state': 'hidden',
                                  'image': None,
                                  #'anchor': 'sw',
                                  'tags'  : ('player-img-clear', 'player-1-img')}}

        rec_2 = {'player-2-rec': {'state'  : 'hidden',
                                  'fill'   : 'black',
                                  'outline': 'white',
                                  'width'  : 5,
                                  'tags'   : ('player-rec-clear', 'player-2-rec')}}
        
        txt_2 = {'player-2-txt': {'state': 'hidden',
                                   'fill': 'white',
                                   'font': font,
                                   'anchor': 'ne',
                                   'tags'  : ('player-txt-clear', 'player-2-txt', 'computer-txt')}}
        
        img_2 = {'player-2-img': {'state' : 'hidden',
                                  'image' : None,
                                  #'anchor': 'se',
                                  'tags'  : ('player-img-clear', 'player-2-img')}}

        self.player.update(txt_1) 
        self.player.update(img_1) 
        self.player.update(rec_1) 
        self.player.update(txt_2) 
        self.player.update(img_2)
        self.player.update(rec_2)  





