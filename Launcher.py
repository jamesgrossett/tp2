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
        self.inventory.pack()

        self.update_values()

    def update_values(self):
        #Update values after a given time interval in ms
        interval = 10

        self.inventory.config(text='Inventory: ' + TelemetryData.getInventory)
        self.after(interval, self.update_values)
        
if __name__ == '__main__':
    app = TelemetryUI()
    app.mainloop()