import tkinter as tk

ROWS = 3
COLS = 3
GRY = 'gray25'
RED = 'red'
GRN = 'green'
BLU = 'blue'


class BoardGUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.box=[None]*9
        self.txt=[None]*9
        self.img=[None]*9
        self.title("Ortho-Matryx Game")
        self.geometry("%sx%s" % (self.winfo_screenwidth(), self.winfo_screenheight()))
        #self.attributes('-fullscreen', True)
        self.frame = tk.Frame(self, bg='black')
        
        
        self._create_matrix()
        self._create_main_menu()
        self._create_avatar_menu()
        self.frame.pack(side="bottom", fill="both", expand=True, anchor='center')     

    def _create_matrix(self):
        h = self.winfo_screenheight() 
        w = self.winfo_screenwidth() 
        w = w - (w-h)
        self.canvas = tk.Canvas( self.frame, 
                                 width=h, 
                                 height=w,
                                 background='black', 
                                 highlightcolor='black',
                                 highlightthickness=0,
                                 borderwidth=0)
        self.canvas.pack(side="bottom")
        
        rect_w = (w / COLS) - 20
        rect_h = (h / ROWS) - 20
        mid = (rect_w / 2)
        print(rect_w)
        print(rect_h)
        print(mid)
        for r in range(ROWS):
            for c in range(COLS):
                x1 = (rect_w * c)
                y1 = (rect_h * r)
                x2 = (rect_w * (c+1))
                y2 = (rect_h * (r+1))
                coord1 = (x1, y1, x2, y2)
                coord2 = (x1+mid, y1+mid)
                self.box[(r*3)+c] = self.canvas.create_oval(coord1, fill=GRY,
                                                            tags='matrix box',outline='black',
                                                            width='10')
                
                self.txt[(r*3)+c] = self.canvas.create_text(coord2, fill='black',
                                                            state='disabled', font='Verdana 35',
                                                            tags='matrix txt', justify='center')
                
                self.img[(r*3)+c] = self.canvas.create_image(coord2, state='disabled',
                                                            tags='matrix img')
                
    def _create_main_menu(self):
        self.canvas.addtag_withtag(newtag='main play', tagOrId=self.txt[0])
        for id in self.box[0:7:3]:
            self.canvas.addtag_withtag(newtag='main green', tagOrId=id)

        self.canvas.addtag_withtag(newtag='main avatar', tagOrId=self.txt[2])
        for id in self.box[2:9:3]:
            self.canvas.addtag_withtag(newtag='main blue', tagOrId=id)
        
        for id in self.box[1:8:3]:
            self.canvas.addtag_withtag(newtag='main default', tagOrId=id)

    def _create_avatar_menu(self):
        for id in self.box[0:6:1]:
            self.canvas.addtag_withtag(newtag='avatar blue', tagOrId=id)
        for id in self.img[0:6:1]:
            self.canvas.addtag_withtag(newtag='avatar img', tagOrId=id)    
        
        self.canvas.addtag_withtag(newtag='avatar play', tagOrId=self.txt[8])
        self.canvas.addtag_withtag(newtag='avatar green', tagOrId=self.box[8])
        self.canvas.addtag_withtag(newtag='avatar back', tagOrId=self.txt[6])
        self.canvas.addtag_withtag(newtag='avatar red', tagOrId=self.box[6])
        self.canvas.addtag_withtag(newtag='avatar default', tagOrId=self.box[7])

    def color_matrix(self, color_string):
        self.canvas.itemconfig('matrix txt', state='disabled')
        self.canvas.itemconfig('matrix img', state='disabled')
        for i in range(ROWS * COLS):
            if (color_string[i] == 'R'):
                color = RED
            elif (color_string[i] == 'G'):
                color = GRN
            elif (color_string[i] == 'B'):
                color = BLU
            else:
                color = GRY
            self.canvas.itemconfig(self.box[i],fill=color)

    def main_menu(self):
        self.canvas.itemconfig('matrix txt', state='disabled')
        self.canvas.itemconfig('matrix img', state='disabled')
        
        self.canvas.itemconfig('main play',state='normal',text="Quick\nPlay")
        self.canvas.itemconfig('main green',fill=GRN)
        self.canvas.itemconfig('main avatar',state='normal',text="Avatar\nMenu")
        self.canvas.itemconfig('main blue',fill=BLU)
        self.canvas.itemconfig('main default',fill=GRY)

    def avatar_menu(self):
        self.canvas.itemconfig('matrix txt', state='disabled')
        self.canvas.itemconfig('matrix img', state='disabled')

        self.canvas.itemconfig('avatar img',state='normal')
        self.canvas.itemconfig('avatar blue',fill=BLU)
        self.canvas.itemconfig('avatar play',state='normal',text="START\nGAME")
        self.canvas.itemconfig('avatar green',fill=GRN)
        self.canvas.itemconfig('avatar back',state='normal',text="MAIN\nMENU")
        self.canvas.itemconfig('avatar red',fill=RED)
        self.canvas.itemconfig('avatar default',fill=GRY)

         
if __name__ == "__main__":
    game = BoardGUI()
    game.avatar_menu()
    game.mainloop()
