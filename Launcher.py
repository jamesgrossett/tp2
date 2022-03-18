from random import randint
import tkinter as tk
import time

import DataHandler
from DataHandler import TelemetryData


class TelemetryUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.data = TelemetryData()
        self.inventory = tk.Label(self, text='Inventory: ' + '0')
        self.errorState = tk.Label(self, text='Error State: ' + 'False')
        self.increment = tk.Button(self, text='Increment Inventory', command=lambda : self.data.increase())

        self.inventory.pack()
        self.errorState.pack()
        self.increment.pack()

        self.update_values()

    def update_values(self):
        #Update values after a given time interval in ms
        interval = 10
        
        #Update inventory value
        self.inventory.config(text='Inventory: ' + str(self.data.getInventory()))

        #Update Error State
        self.errorState.config(text='Error State: ' + str(self.data.getErrorState()))

        self.after(interval, self.update_values)
        
if __name__ == '__main__':
    app = TelemetryUI()
    app.mainloop()