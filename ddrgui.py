# Main UI
# Needs to: run on Raspberry Pi power on (exec UNIX command), take button input from several different I/O pins (? depends on how we implement), access and discriminate between each pin,
# change color depending on what button was pressed

# for now, just changes color based on button input, button needs to execute a C++/C file in the final version of product

import tkinter as tk

def ChangeRed():
    print("Red button pressed")
    root.configure(bg = 'red')

def ChangeBlue():
    print("Blue button pressed")
    root.configure(bg = 'blue')

def ChangeYellow():
    print("Yellow button pressed")
    root.configure(bg = 'yellow')

root = tk.Tk()

root.title('DDR')
root.geometry('400x400') # in final version, needs to be fixed to size of monitor, borderless, etc.

redButton = tk.Button(root, text = "Red", command = lambda:ChangeRed())
blueButton = tk.Button(root, text = "Blue", command = lambda:ChangeBlue())
yellowButton = tk.Button(root, text = "Yellow", command = lambda:ChangeYellow())

redButton.pack()
blueButton.pack()
yellowButton.pack()

root.mainloop()