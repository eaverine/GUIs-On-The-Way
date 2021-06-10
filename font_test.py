import tkinter as tk
from tkinter.font import Font
from tkinter.font import nametofont

root = tk.Tk()

default_font = nametofont('TkDefaultFont')
default_font.config(family = 'Helvetica', size = 32)

tk.Label(text = 'Feeling Groovy').pack()

labelfont = Font(family = 'Courier', size = 30, weight = 'bold' \
                 ,slant = 'roman', underline = False, overstrike = False)
tk.Label(text = 'Using the Font class', font = labelfont).pack()

def toggle_strike():
    labelfont['overstrike'] = not labelfont['overstrike']

tk.Button(text = 'Toggle Overstrike', command = toggle_strike, font = (12)).pack()

root.mainloop()
