# Main UI REV 1.4
# 1.4 Changes: display avatars and corresponding buttons to save path
# 2.0 revision will come upon refactoring into OOP approach

# TODO Next Revision: split into multiple files (incorrect assumption on Python file importing previously), implement scoreboard frame, stylize mainMenu frame

# On Pi, need to install modules: tkinter, Pillow
# cmd line inputs: 
# python3 -m pip install pillow

import os
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import Canvas, Frame, ttk

# create root and frames globally to ensure functions can access data
root = tk.Tk()
mainMenu = Frame(root)
avatarSelect = Frame(root)
gameScreen = Frame(root)

def SelectAvatar(path):
    print("Select this avatar: " + path)

def LaunchAvatar():
    print("Entered Avatar Select")
    avatarList = os.listdir(r'C:\Users\Ryan\Desktop\capstone_guidev\avatar_pics')
    labelList = []; buttonList = []; columnNum = 0; rowNum = 0
    for i in range(len(avatarList)):
        def func(x=i):
            return SelectAvatar(r'C:\Users\Ryan\Desktop\capstone_guidev\avatar_pics\\'+avatarList[x])
        temp = ImageTk.PhotoImage(Image.open(r'C:\Users\Ryan\Desktop\capstone_guidev\avatar_pics\\'+avatarList[i]).resize((100,100)))
        labelList.append(tk.Label(avatarSelect))
        labelList[i].image = temp
        labelList[i].configure(image = temp)
        labelList[i].grid(row=rowNum, column=columnNum, padx=80, pady=80)
        buttonList.append(tk.Button(avatarSelect, text="Select", command = func))
        buttonList[i].grid(row=rowNum, column=columnNum)
        if columnNum == 2:
            rowNum += 1
            columnNum = 0
        else:
            columnNum += 1

    avatarSelect.pack(fill='both', expand=1)
    mainMenu.pack_forget()
    gameScreen.pack_forget()

def LaunchQP():
    print("Entered Quick Play")
    gameScreen.pack(fill='both', expand=1)
    LoadMatrix()
    mainMenu.pack_forget()
    avatarSelect.pack_forget()

def LaunchMM():
    print("Entered mainMenu")
    mainMenu.pack(fill='both', expand=1)
    avatarSelect.pack_forget()

    # delete only the Canvas widget in gameLoop: deleting the rest blows up the whole GUI since frame is only initialized once
    for widget in gameScreen.winfo_children():
        if (type(widget) == Canvas):
            widget.destroy()
            break
    
    gameScreen.pack_forget()

def LoadMatrix():
    xIter = 0; yIter = 0
    matrix = tk.Canvas(gameScreen, bg="white", height=300, width=300)

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

def main():

    root.title('Main Menu')
    root.geometry('800x800') # in final version, needs to be fixed to size of monitor, borderless, etc.

    # initialize frame displays
    labelGS = tk.Label(gameScreen, text="Displaying game screen", font="Helvetica")
    labelGS.pack()

    returnMM_GS = tk.Button(gameScreen, text = "Return to Main Menu", command = lambda:LaunchMM())
    returnMM_GS.pack()
    returnMM_AS = tk.Button(avatarSelect, text = "Return to Main Menu", command = lambda:LaunchMM())
    returnMM_AS.grid(row = 10, column = 1)

    # title: thinking about making something in GIMP or photoshop instead of just a plain label
    titleVar = tk.StringVar()
    mmTitle = ttk.Label(mainMenu, textvariable=titleVar, font="Helvetica", relief=tk.RAISED)
    titleVar.set("Ortho-Matryx")

    avatarButton = tk.Button(mainMenu, text = "Select Avatar", command = lambda:LaunchAvatar())
    qpButton = tk.Button(mainMenu, text = "Quick Play", command = lambda:LaunchQP())

    # load mainMenu frame
    mainMenu.pack(fill='both', expand=1)

    mmTitle.place(relx=0.5, rely = 0.4, anchor = tk.CENTER)
    avatarButton.place(relx=0.5, rely = 0.5, anchor = tk.CENTER)
    qpButton.place(relx=0.5, rely = 0.58, anchor = tk.CENTER)

    # makes gui borderless: don't do this yet since it makes development harder
    #root.overrideredirect(True)
    
    root.mainloop()

if __name__ == '__main__':
    main()