import tkinter as tk
import time

import DataHandler
from DataHandler import TelemetryData


class TelemetryUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.inventory = tk.Label(self, text='')
        self.inventory.pack()

        self.update_clock()

    def update_values(self):

        #Call this function again after 10ms
        self.after(10, self.update_values)
        
if __name__ == '__main__':
    data = TelemetryData()
    app = TelemetryUI()
    app.mainloop()