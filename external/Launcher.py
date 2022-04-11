from random import randint
import tkinter as tk

import time
from UDPListener import Listener

import DataHandler
from DataHandler import TelemetryData
from UDPListener import Listener


class TelemetryUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #GUI config
        self.bgcolour = 'black'
        self.fgcolour = 'blue'
        self.textstyle = ('Calibri', 25)
        self.configure(bg=self.bgcolour)
        self.title('Telemetry Display')
        self.geometry("600x250")

        #Initialise telemetry data class
        self.data = TelemetryData()
        self.connection = Listener()

        #Default choice for communcation method
        self.connectionVariable = tk.StringVar(self)
        self.connectionVariable.set("Select")

        #Initialising tkinter widgets
        self.inventory = tk.Label(self, text='Inventory: ', bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
        self.inventoryValue = tk.Label(self, text=self.data.getInventory(), bg=self.bgcolour, fg='red', font=self.textstyle)
        self.errorLabel = tk.Label(self, text='Error State: ', bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
        self.errorState = tk.Label(self, text=self.data.getErrorState(), bg=self.bgcolour, fg='red', font=self.textstyle)
        self.increment = tk.Button(self, text='Increment Inventory', command=lambda : self.data.increase(), bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
        self.decrement = tk.Button(self, text='Decrement Inventory', command=lambda : self.data.decrease(), bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
        self.connectionMethod = tk.OptionMenu(self, self.connectionVariable, "Bluetooth", "WiFi")
        self.connectionMethod.config(bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
        self.bluetoothLabel = tk.Label(self, text='Bluetooth: ', bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
        self.wifiLabel = tk.Label(self, text='WiFi: ', bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
        self.bluetoothStatus = tk.Label(self, text='PLACEHOLDER', bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
        self.wifiStatus = tk.Label(self, text='PLACEHOLDER', bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
        dropDown = self.nametowidget(self.connectionMethod.menuname)
        dropDown.config(bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
        
        #Grid management
        self.inventory.grid(column=0, row=0)
        self.inventoryValue.grid(column=1, row=0)
        self.errorLabel.grid(column=0, row=1)
        self.errorState.grid(column=1, row=1)
        self.increment.grid(column=0, row=2, columnspan=2)
        self.decrement.grid(column=0, row=3, columnspan=2)
        self.bluetoothLabel.grid(column=3, row=0)
        self.wifiLabel.grid(column=3, row=1)
        self.bluetoothStatus.grid(column=4, row=0)
        self.wifiStatus.grid(column=4, row=1)
        self.connectionMethod.grid(column=3, row=2, columnspan=2)

        self.update_values()

    def update_values(self):
        #Update values after a given time interval in ms
        interval = 1000

        #Recieve new data via UDP connection
        inventory = self.connection.recieve()
        bluetoothStatus = False
        wifiStatus = True
        errorState = False
        
        #Update inventory value
        self.inventoryValue.config(text=str(inventory))
        if (inventory > 0):
            self.inventoryValue.config(fg='green')
        else:
            self.inventoryValue.config(fg='red')

        #Update Error State
        self.errorState.config(text=str(errorState))
        if (errorState):
            self.errorState.config(fg='red')
        else:
            self.errorState.config(fg='green')

        self.after(interval, self.update_values)

        #Update bluetooth and wifi status indicators
        self.bluetoothStatus.config(text=str(bluetoothStatus))
        if (bluetoothStatus):
            self.bluetoothStatus.config(fg='green')
        else:
            self.bluetoothStatus.config(fg='red')

        self.wifiStatus.config(text=str(wifiStatus))
        if (wifiStatus):
            self.wifiStatus.config(fg='green')
        else:
            self.wifiStatus.config(fg='red')

        
if __name__ == '__main__':
    app = TelemetryUI()
    app.mainloop()