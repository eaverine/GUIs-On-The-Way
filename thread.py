from time import sleep
import tkinter as tk
from tkinter import ttk
from threading import Thread

def print_slowly(string):
    words = string.split()

    for word in words:
        sleep(1)
        print(word)

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.text = tk.StringVar()
        ttk.Entry(self, textvariable = self.text).pack()

        ttk.Button(self, text = 'Run Unthreaded', command = self.print_unthreaded).pack()
        ttk.Button(self, text = 'Run Threaded', command = self.print_threaded).pack()
        

    def print_unthreaded(self):
        print_slowly(self.text.get())

    def print_threaded(self):
        thread = Thread(target = print_slowly, args = (self.text.get(),) )
        thread.start()

App().mainloop()




"""import tkinter as tk
from time import sleep

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.status = tk.StringVar()

        tk.Label(self, textvariable = self.status).pack()
        tk.Button(self, text = 'Run Process', command = self.run_process).pack()

    def run_process(self):
        self.status.set('Starting Process')
        
        self.after(50, self._run_processes)

    def _run_processes(self):
        for i in range(1,5):
            self.status.set(f'Phase {i}')
            self.update_idletasks()
            self.process_phase(i, 2)

        self.status.set('Complete')

    def process_phase(self, n, length):
        sleep(length)
                        



App().mainloop()"""
