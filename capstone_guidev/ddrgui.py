# Main UI REV 1.2
# 1.2 Changes: framework for avatar selection/gameloop screen

# TODO Next Revision: add GUI class (with args/kwargs), add representation for light matrix in gameLoop, add functionality to return to MM after avatar screen/gameLoop

# Needs to: run on Raspberry Pi power on (exec UNIX command), take button input from several different I/O pins (? depends on how we implement), access and discriminate between each pin,
# change color depending on what button was pressed

import tkinter as tk
from tkinter import Frame

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
    mainMenu.pack_forget()
    avatarSelect.pack_forget()

# TODO: add mainMenu frame function to enter in the gameScreen/avatarSelect frames

def main():

    root.title('Main Menu')
    root.geometry('400x400') # in final version, needs to be fixed to size of monitor, borderless, etc.

    # initialize frame displays
    labelQP = tk.Label(gameScreen, text="Displaying game screen", font="Helvetica")
    labelQP.pack()
    labelAvatar = tk.Label(avatarSelect, text="Displaying avatar select", font="Helvetica")
    labelAvatar.pack()

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