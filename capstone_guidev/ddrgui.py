# Main UI REV 1.1
# 1.1 Changes: gui launch refactored into main function, gui title change, buttons renamed to pertinent functions/centered, add main menu text

# TODO Next Revision: multiple window navigation (use frames)

# Needs to: run on Raspberry Pi power on (exec UNIX command), take button input from several different I/O pins (? depends on how we implement), access and discriminate between each pin,
# change color depending on what button was pressed

# for now, just changes color based on button input, button needs to execute a C++/C file in the final version of product

import tkinter as tk

root = tk.Tk()

def LaunchAvatar():
    print("Entered Avatar Select")

def LaunchQP():
    print("Entered Quick Play")

def main():

    root.title('Main Menu')
    root.geometry('400x400') # in final version, needs to be fixed to size of monitor, borderless, etc.

    # title: thinking about making something in GIMP or photoshop instead of just a plain label
    titleVar = tk.StringVar()
    mmTitle = tk.Label(root, textvariable=titleVar, font="Helvetica", relief=tk.RAISED)
    titleVar.set("Ortho-Matryx")

    avatarButton = tk.Button(root, text = "Select Avatar", command = lambda:LaunchAvatar())
    qpButton = tk.Button(root, text = "Quick Play", command = lambda:LaunchQP())

    mmTitle.place(relx=0.5, rely = 0.4, anchor = tk.CENTER)
    avatarButton.place(relx=0.5, rely = 0.5, anchor = tk.CENTER)
    qpButton.place(relx=0.5, rely = 0.58, anchor = tk.CENTER)

    # makes gui borderless: don't do this yet since it makes development harder
    #root.overrideredirect(True)
    
    root.mainloop()

if __name__ == '__main__':
    main()