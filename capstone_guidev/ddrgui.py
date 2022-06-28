# Main UI REV 2.0
# 2.0 Changes: GUI refactored into OOP approach
# OOP allows for easier file splitting for organization, improved readability, etc.

# TODO Next Revision: implement Scoreboard class, split files, stylize MainMenu class

# On Pi, need to install modules: tkinter, Pillow
# cmd line inputs: 
# python3 -m pip install pillow

import os
import tkinter as tk
from PIL import ImageTk, Image

LARGE_FONT= ("Verdana", 12)

class orthoGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}

        for F in (MainMenu, AvatarSelect, GameLoop):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainMenu)

        self.title("Ortho-Matryx")
        self.geometry('800x800')

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # replace with GIMP/PhotoShop created title
        titleVar = tk.StringVar()
        titleVar.set("Ortho-Matryx")
        mmTitle = tk.Label(self, textvariable=titleVar, font="Helvetica", relief=tk.RAISED)

        avatarButton = tk.Button(self, text = "Select Avatar", command = lambda:controller.show_frame(AvatarSelect))
        qpButton = tk.Button(self, text = "Quick Play", command = lambda:controller.show_frame(GameLoop))

        mmTitle.pack()
        avatarButton.pack()
        qpButton.pack()

class AvatarSelect(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        avatarList = os.listdir(r'C:\Users\Ryan\Desktop\capstone_guidev\avatar_pics')
        labelList = []; buttonList = []; columnNum = 0; rowNum = 0
        for i in range(len(avatarList)):
            def func(x=i):
                return SelectAvatar(r'C:\Users\Ryan\Desktop\capstone_guidev\avatar_pics\\'+avatarList[x])
            temp = ImageTk.PhotoImage(Image.open(r'C:\Users\Ryan\Desktop\capstone_guidev\avatar_pics\\'+avatarList[i]).resize((100,100)))
            labelList.append(tk.Label(self))
            labelList[i].image = temp
            labelList[i].configure(image = temp)
            labelList[i].grid(row=rowNum, column=columnNum, padx=80, pady=80)
            buttonList.append(tk.Button(self, text="Select", command = func))
            buttonList[i].grid(row=rowNum, column=columnNum)
            if columnNum == 2:
                rowNum += 1
                columnNum = 0
            else:
                columnNum += 1

        returnMM_AS = tk.Button(self, text = "Return to Main Menu", command = lambda:controller.show_frame(MainMenu))
        returnMM_AS.grid(row = 10, column = 1)

class GameLoop(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        xIter = 0; yIter = 0
        matrix = tk.Canvas(self, bg="white", height=300, width=300)

        # probably not efficient: consider refactoring if performance taking hits
        # doesn't matter what color the squares are for now: data from the MCU will decide that in a later revision
        for i in range(9):
            matrix.create_rectangle(xIter, yIter, xIter+100, yIter+100, fill='red')
            if xIter == 200:
                yIter += 100
                xIter = 0
            else:
                xIter += 100
        matrix.pack(anchor=tk.CENTER)

        returnMM_GS = tk.Button(self, text = "Return to Main Menu", command = lambda:controller.show_frame(MainMenu))
        returnMM_GS.pack()

def SelectAvatar(path):
     print("Select this avatar: " + path)

if __name__ == "__main__":
    app = orthoGUI()
    app.mainloop()