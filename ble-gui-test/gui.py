import tkinter as tk
import asyncio
from config import CanvasConfigs

class GUI(tk.Canvas):
    
    def __init__(self, parent, interval=1/120):
        side = parent.winfo_height()
        super().__init__(parent, width=side, height=side, bg = 'black', highlightthickness=0)
        self.pack()
        
        self.screen = CanvasConfigs()
        self.interval = interval
        self.background=[]  
        self.background_txt=[]  
        self.background_img=[]
        self.button=[] 
        self.button_txt=[] 
        self.button_img=[]

        self.create_background_items(side)
        self.create_button_items(side)
    

    def create_background_items(self, side):

        self.background.append(
            self.create_rectangle( 
                0, 0, side, side, 
                tags=self.screen.tags['background'] 
            )
        )
        self.background_txt.append(
            self.create_text( 
                side/2, side/2, fill='black', 
                font='Verdana 30', justify='left', 
                tags=self.screen.tags['background text'] 
            )
        )
        self.background_img.append(
            self.create_image( 
                side/2, side/2,
                tags=self.screen.tags['background image'] 
            )
        )


    def create_button_items(self, side):

        cell = side / 3 
        midd = cell / 2  
        bounds = [] ; center = []

        for col in range(self.screen.matrix_cols):
            for row in range(self.screen.matrix_rows):
                
                x1, y1 = (cell*row), (cell*col) 
                x2, y2 = (x1+cell), (y1+cell)
                x3, y3 = (x1+midd), (y1+midd)

                bounds.append((x1, y1, x2, y2))
                center.append((x3, y3))


        for i in range(self.screen.matrix_size):

            self.button.append( 
                self.create_oval( 
                    bounds[i],
                    outline='black', width='10', 
                    tags=self.screen.tags['button'][i] 
                )
            )
            self.button_txt.append(
                self.create_text( 
                    center[i], fill='black', 
                    font='Verdana 35', justify='center', 
                    tags=self.screen.tags['button text'][i] 
                )
            )
            self.button_img.append(
                self.create_image( 
                    center[i], 
                    tags=self.screen.tags['button image'][i] 
                )
            )


    def clear(self):
        for key,value in self.screen.configs['clear'].items():
            self.itemconfig(**value)


    def set_config(self, config, clear_screen):
        if clear_screen == True:
            self.clear()
        for key,value in config.items():
            self.itemconfig(**value)


    async def set_color(self, color_string):
        await asyncio.sleep(self.interval)
        self.clear()
        for i, letter in enumerate(color_string):
            if letter in self.screen.colors:
                color = self.screen.colors[letter] 
            else:
                color = self.screen.colors['default color']
            self.itemconfig(self.button[i],fill=color, state='normal')


    async def title(self):
        await self.set_color(self.screen.colors['title'])
        self.set_config(self.screen.configs['title'], False)


    async def menu(self):
        await self.set_color(self.screen.colors['menu'])
        self.set_config(self.screen.configs['menu'], False)    


    async def avatar(self):
        await self.set_color(self.screen.colors['avatar'])
        self.set_config(self.screen.configs['avatar'], False)


    async def highscore(self):
        await asyncio.sleep(self.interval)
        scores = ''
        file = open('/home/nt-user/workspace/new-gui/score.txt', 'r')
        for line in file:
            scores = scores + line.replace(' ', '\t')
        self.screen.update_highscore(scores)
        self.set_config(self.screen.configs['highscore'], True)


    async def updater(self):
        while True:
            self.update()
            await asyncio.sleep(self.interval)
