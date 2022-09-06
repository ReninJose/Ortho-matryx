from settings import Clear, Title, Menu, Avatar, HighScore
from tag import Tags
from colors import ColorDict

class CanvasConfigs:
    def __init__(self):
        self.tags = Tags
        self.colors = ColorDict
        self.matrix_size = 9
        self.matrix_rows = 3
        self.matrix_cols = 3
        self.configs = {}
        
        for Screen in (Clear(), Title(), Menu(), Avatar(), HighScore()):
            for i in range(len(Screen.settings)):
                Screen.create(i, *Screen.settings[i])
            self.configs.update({Screen.name: Screen.configs})
    
    def update_highscore(self, score):
        self.configs['highscore'][1]['text'] = score

