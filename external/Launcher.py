from multiprocessing import parent_process
from random import randint
import tkinter as tk
import socket
import time
from turtle import bgcolor
from UDPListener import Listener
import DataHandler
from DataHandler import TelemetryData
from UDPListener import Listener


class TelemetryUI(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        
        self.parent = parent

        #GUI config
        self.bgcolour = 'black'
        self.fgcolour = 'blue'
        self.textstyle = ('Calibri', 25)
        self.configure(bg=self.bgcolour)
        parent.configure(bg=self.bgcolour)
        parent.title('Telemetry Display')
        parent.geometry("600x250")

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
        self.inventoryAdjust = tk.Button(self, text='Adjust Inventory', command=self.adjust_inventory, bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
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
        self.inventoryAdjust.grid(column=0, row=2, columnspan=2)
        self.bluetoothLabel.grid(column=3, row=0)
        self.wifiLabel.grid(column=3, row=1)
        self.bluetoothStatus.grid(column=4, row=0)
        self.wifiStatus.grid(column=4, row=1)
        self.connectionMethod.grid(column=3, row=2, columnspan=2)

        #Initialise inventory value at startup
        self.inventory = 0
        self.update_values()

    def update_values(self):
        #Update values after a given time interval in ms
        interval = 100

        #Initialise key and value to be invalid
        key, value = 0, 0

        #Recieve new data via UDP connection
        try:
            key, value = self.connection.recieve_keyvalue()
        except:
            print('Failed to get data')
            
        if key == 1: #Key of 1 indicates inventory value
            self.inventory = value
        elif key == 2: #Key of 2 indicates error status
            self.errorState = value
        elif key == 3: #Key of 3 indicates outbound inventory and should be ignored
            print(value)
        else:
            print('Invalid key')


        bluetoothStatus = False
        wifiStatus = True
        errorState = False
        
        #Update inventory value
        self.inventoryValue.config(text=str(self.inventory))
        if (self.inventory > 0):
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

    def adjust_inventory(self):
        self.top = tk.Toplevel(self.parent)
        self.top.configure(bg=self.bgcolour)
        self.top.title('Inventory Adjustment')
        self.top.geometry('250x250')
        adjustLabel = tk.Label(self.top, text = 'Enter new inventory value', bg=self.bgcolour, fg=self.fgcolour)
        self.inputbox = tk.Text(self.top, bg=self.bgcolour, fg=self.fgcolour, height=5, width=20)
        sendButton = tk.Button(self.top, text='Send', bg=self.bgcolour, fg=self.fgcolour, command = self.send_inventory)

        adjustLabel.pack()
        self.inputbox.pack()
        sendButton.pack()
    
    def send_inventory(self):
        #Gets input inventory value and removes newline
        value = int(self.inputbox.get("1.0", 'end-1c'))
        #Sends inventory data to rasberry pi
        self.connection.send_keyvalue(3, value)
        self.top.destroy()

        
if __name__ == '__main__':
    root = tk.Tk()
    TelemetryUI(root).pack()
    root.mainloop()