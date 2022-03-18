from random import randint
import tkinter as tk

import time

import DataHandler
from DataHandler import TelemetryData


class TelemetryUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #GUI config
        self.bgcolour = 'black'
        self.fgcolour = 'blue'
        self.configure(bg=self.bgcolour)
        self.geometry("300x250")

        #Initialise telemetry data class
        self.data = TelemetryData()

        #Default choice for communcation method
        self.connectionVariable = tk.StringVar(self)
        self.connectionVariable.set("Select")

        #Initialising tkinter widgets
        self.inventory = tk.Label(self, text='Inventory: ', bg=self.bgcolour, fg=self.fgcolour, font=('Calibri', 25))
        self.inventoryValue = tk.Label(self, text=self.data.getInventory(), bg=self.bgcolour, fg='red', font=('Calibri', 25))
        self.errorLabel = tk.Label(self, text='Error State: ', bg=self.bgcolour, fg=self.fgcolour, font=('Calibri', 25))
        self.errorState = tk.Label(self, text=self.data.getErrorState(), bg=self.bgcolour, fg='red', font=('Calibri', 25))
        self.increment = tk.Button(self, text='Increment Inventory', command=lambda : self.data.increase(), bg=self.bgcolour, fg=self.fgcolour, font=('Calibri', 25))
        self.connectionMethod = tk.OptionMenu(self, self.connectionVariable, "Bluetooth", "WiFi")
        self.connectionMethod.config(bg=self.bgcolour, fg=self.fgcolour, font=('Calibri', 25))
        dropDown = self.nametowidget(self.connectionMethod.menuname)
        dropDown.config(bg=self.bgcolour, fg=self.fgcolour, font=('Calibri', 25))
        
        #Grid management
        self.inventory.grid(column=0, row=0)
        self.inventoryValue.grid(column=1, row=0)
        self.errorLabel.grid(column=0, row=1)
        self.errorState.grid(column=1, row=1)
        self.increment.grid(column=0, row=2, columnspan=2)
        self.connectionMethod.grid(column=0, row=3, columnspan=2)

        self.update_values()

    def update_values(self):
        #Update values after a given time interval in ms
        interval = 10
        
        #Update inventory value
        self.inventoryValue.config(text=str(self.data.getInventory()))
        if (self.data.getInventory() > 0):
            self.inventoryValue.config(fg='green')
        else:
            self.inventoryValue.config(fg='red')

        #Update Error State
        self.errorState.config(text=str(self.data.getErrorState()))
        if (self.data.getErrorState()):
            self.errorState.config(fg='red')
        else:
            self.errorState.config(fg='green')

        self.after(interval, self.update_values)
        
if __name__ == '__main__':
    app = TelemetryUI()
    app.mainloop()