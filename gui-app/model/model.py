from util.player import Player
from util.color  import DEFAULT



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

LETTERS = [
    'A', 'B', 'C', 'D', 
    'E', 'F', 'G', 'H', 
    'I', 'J', 'K', 'L', 
    'M', 'N', 'O', 'P', 
    'Q', 'R', 'S', 'T', 
    'U', 'V', 'W', 'X', 
    'Y', 'Z', ' '
]

class Model:

    game_run    = False
    game_type   = None
    quickplay   = True
    multiplayer = False

    pattern = [DEFAULT, DEFAULT]
    winning = None

    player_1 = Player(1, 'player-1-txt', 'player-1-img', 'player-1-rec')
    player_2 = Player(2, 'player-2-txt', 'player-2-img', 'player-2-rec')
    computer = Player(0, 'computer-txt', 'player-2-img', 'player-2-rec')
    active_player = player_1.info
    highlight = None

    ctrl = None
    sub  = None
    loop = None
    

    def __init__(self, config, color, event=[], music=None):
        self.config = config
        self.event  = event
        self.color  = color
        self.music  = music
        self._start()

    def _start(self):
        self.ctrl.model = self
        self._clear_event()
        self._view()
        self._event()
        self._song()

    def update(self):
        self._view()
        self._event()

    def _view(self): 
        self.ctrl.show_flag.set()

    def clear_event(self):
        self.event = []
        self.ctrl.event_dict = self.event

    def _clear_event(self):
        self.ctrl.event_dict = {}
                
    def _event(self):
        self.ctrl.event_dict = self.event
        #for E in self.event: self.ctrl.set_event(**E)
        
    def _song(self):
        if self.music != None:
            self.ctrl.theme_song(self.music)

    @classmethod
    def player_avatar(cls, index):
        avatar = cls.ctrl.panel_avatar[index]
        cls.active_player['avatar']  = avatar
        cls.active_player['avindex'] = index

    @classmethod
    def scoreboard_avatar(cls, index):
        avatar = cls.ctrl.score_avatar[index]
        return avatar

    @classmethod
    def font(cls, size=30, style='normal'):
        return cls.ctrl.set_font(size=size, style=style)

    @classmethod
    def new_model(cls, new, *args, **kwargs):
        cls.sub[new]()
        
    @classmethod
    def new_game(cls, *args, **kwargs):
        cls.sub[cls.game_type]()

    @classmethod
    def reset_game_data(cls):
        cls.game_run    = False
        cls.game_type   = None
        cls.quickplay   = True
        cls.multiplayer = False

        cls.pattern = [DEFAULT, DEFAULT]
        cls.winning = None

        cls.player_1.reset()
        cls.player_2.reset()
        cls.computer.reset()
        cls.computer.info['avatar'] = cls.ctrl.panel_avatar[5]
        cls.active_player = cls.player_1.info
        cls.highlight = None
        
    @classmethod
    def ble_disconnect(cls, *args, **kwargs):
        cls.loop.create_task(cls.ctrl.ble.disconnect())