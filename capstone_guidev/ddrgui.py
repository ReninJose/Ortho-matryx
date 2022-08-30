# Main UI REV 2.30
# 2.30 Changes: Error handling in main class and avatar class, widget rearrangement, fullscreen w/ toolbar (for now)

# TODO Next Revision: begin to stylize background + widgets before adding gui nav functionality, rearrange widgets in avatarSelect screen

# On Pi, need to install modules: tkinter, Pillow
# cmd line inputs: 
# python3 -m pip install pillow

import os
import time
import threading
import subprocess
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

LARGE_FONT= ("Verdana", 12)
AVATAR_PATH = r'/home/ryanw5758/Desktop/Ortho-matryx-main/capstone_guidev/avatar_pics/'

class orthoGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        WIDTH = self.winfo_screenwidth()
        HEIGHT = self.winfo_screenheight()

        self.geometry("%dx%d" % (WIDTH, HEIGHT))
        container = tk.Frame(self, width=WIDTH, height=HEIGHT)
        container.pack(side="top", fill="both", expand=True)
        container.config(height=HEIGHT, width=WIDTH)

        self.frames = {}

        try:
            for F in (MainMenu, AvatarSelect, GameLoop, Scoreboard):
                frame = F(container, self)
                self.frames[F] = frame
                #frame.grid(row=0, column=0, sticky="nsew")
                frame.place(x=0, y=0, anchor="nw", width=WIDTH, height=HEIGHT)
            self.show_frame(MainMenu)
        except KeyError as err:
            print("Error: Display frame not found in list")
            print(format(err))

        self.title("Ortho-Matryx")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # replace with GIMP/PhotoShop created title
        mmTitle = ttk.Label(self, text = "Ortho-Matryx", font="Helvetica")

        avatarButton = ttk.Button(self, text = "Select Avatar", command = lambda:controller.show_frame(AvatarSelect))
        qpButton = ttk.Button(self, text = "Quick Play", command = lambda:controller.show_frame(GameLoop))

        mmTitle.place(relx=0.5,rely=0.3)
        avatarButton.place(relx=0.5,rely=0.5)
        qpButton.place(relx=0.5,rely=0.7)

class AvatarSelect(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        # change paths depending on branch/system currently running the program
        avatarList = os.listdir(AVATAR_PATH)
        labelList = []; buttonList = []; columnNum = 0; rowNum = 0
        try:
            for i in range(len(avatarList)):
                def func(x=i):
                    return SelectAvatar(AVATAR_PATH+avatarList[x])
                temp = ImageTk.PhotoImage(Image.open(AVATAR_PATH+avatarList[i]).resize((100,100)))
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
        except IndexError as err:
            print("Error: Accessing avatar element out of range")
            print(format(err))

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
        matrix.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        WriteSB('Ryan', 4)

        toScoreboard = tk.Button(self, text="Display scoreboard", command = lambda:controller.show_frame(Scoreboard))
        toScoreboard.place(relx = 0.5, rely = 0.7, anchor = tk.CENTER)
        returnMM = tk.Button(self, text = "Return to Main Menu", command = lambda:controller.show_frame(MainMenu))
        returnMM.place(relx = 0.5, rely = 0.8, anchor = tk.CENTER)

class Scoreboard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        scoreboardLabel = tk.Label(self, text = "Scoreboard", font=LARGE_FONT)
        scoreboardLabel.pack()

        with open(r'/home/ryanw5758/Desktop/Ortho-matryx-main/backend/score_board/sb.txt', 'r') as f:
            tk.Label(self, text = f.read()).pack()

        returnMM = tk.Button(self, text = "Return to Main Menu", command = lambda:[controller.show_frame(MainMenu)])
        returnMM.pack()

def WriteSB(name, score):
    print("Writing name to scoreboard: " + name)
    scoreStr = str(score)
    print("Writing score to scoreboard: " + scoreStr)
    subprocess.call(['/home/ryanw5758/Desktop/Ortho-matryx-main/backend/backend', 'sb', name, scoreStr])
    time.sleep(1)

def SelectAvatar(path):
     print("Select this avatar: " + path)
  
if __name__ == "__main__":
    app = orthoGUI()
    app.mainloop()
