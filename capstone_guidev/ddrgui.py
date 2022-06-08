# Main UI REV 1.3
# 1.3 Changes: functionality to return to main menu, matrix representation with Canvas widget on gameLoop screen
# refactor into OOP approach: more readable and easier to edit frames between functions

# TODO Next Revision: displaying avatars on avatar select screen (store path in variable most likely)
# refactor into OOP approach: more readable and easier to edit frames between functions

import tkinter as tk
from tkinter import Canvas, Frame

# create root and frames globally to ensure functions can access data
root = tk.Tk()
mainMenu = Frame(root)
avatarSelect = Frame(root)
gameScreen = Frame(root)

def LaunchAvatar():
    print("Entered Avatar Select")
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

    # delete only the Canvas widget: deleting the rest blows up the whole GUI since frame is only initialized once
    for widget in gameScreen.winfo_children():
        if (type(widget) == Canvas):
            widget.destroy()
            break

    gameScreen.pack_forget()

def LoadMatrix():
    xIter = 0; yIter = 0
    matrix = tk.Canvas(gameScreen, bg="white", height=250, width=300)

    # probably not efficient: refactor in next revision
    # doesn't matter what color the squares are for now: data from the MCU will decide that in a later revision
    for i in range(9):
        matrix.create_rectangle(xIter, yIter, xIter+20, yIter+20, fill='red')
        if xIter == 40:
            yIter += 20
            xIter = 0
        else:
            xIter += 20
    matrix.pack()

def main():

    root.title('Main Menu')
    root.geometry('400x400') # in final version, needs to be fixed to size of monitor, borderless, etc.

    # initialize frame displays
    labelGS = tk.Label(gameScreen, text="Displaying game screen", font="Helvetica")
    labelGS.pack()
    labelAvatar = tk.Label(avatarSelect, text="Displaying avatar select", font="Helvetica")
    labelAvatar.pack()

    returnMM_GS = tk.Button(gameScreen, text = "Return to Main Menu", command = lambda:LaunchMM())
    returnMM_GS.pack()
    returnMM_AS = tk.Button(avatarSelect, text = "Return to Main Menu", command = lambda:LaunchMM())
    returnMM_AS.pack()

    # title: thinking about making something in GIMP or photoshop instead of just a plain label
    titleVar = tk.StringVar()
    mmTitle = tk.Label(mainMenu, textvariable=titleVar, font="Helvetica", relief=tk.RAISED)
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