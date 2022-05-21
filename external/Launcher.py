from multiprocessing import parent_process
from random import randint
import tkinter as tk
import socket
import time
from turtle import bgcolor
from webbrowser import get
from UDPListener import Listener
from UDPListener import Listener
from BTListener import BluetoothListener


class TelemetryUI(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        
        self.parent = parent

        #GUI config
        self.bgcolour = 'black'
        self.fgcolour = 'blue'
        self.textstyle = ('Calibri', 25)
        self.configure(bg=self.bgcolour)
        self.parent.configure(bg=self.bgcolour)
        self.parent.title('Telemetry Display')
        self.parent.geometry("600x250")

        #Initialise connection managers (UDP and BT)
        self.UDPListener = Listener()
        self.BTListener = BluetoothListener()

        #Initialise variable values on startup
        self.inventory = 0
        self.bluetoothState = False
        self.wifiState= True
        self.errorState = False

        #Default choice for communcation method
        self.connectionVariable = tk.StringVar(self)
        self.connectionVariable.set("Bluetooth")

        #Tkinter labels initialised here
        self.errorLabel = tk.Label(self, text='Error State: ', bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
        self.errorStateValue = tk.Label(self, text=self.errorState, bg=self.bgcolour, fg='red', font=self.textstyle)
        self.inventoryLabel = tk.Label(self, text='Inventory: ', bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
        self.inventoryValue = tk.Label(self, text=self.inventory, bg=self.bgcolour, fg='red', font=self.textstyle)
        self.bluetoothLabel = tk.Label(self, text='Bluetooth: ', bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
        self.wifiLabel = tk.Label(self, text='WiFi: ', bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
        self.bluetoothStatus = tk.Label(self, text=self.bluetoothState, bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
        self.wifiStatus = tk.Label(self, text=self.wifiState, bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
        
        #Tkinter buttons initiaised here
        self.inventoryAdjust = tk.Button(self, text='Adjust Inventory', command=self.adjust_inventory, bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
        self.bluetoothConnect = tk.Button(self, text = 'Connect', command=self.BTListener.BTconnect, bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)   
        
        #Tkinter drop down menus initialised here
        self.connectionMethod = tk.OptionMenu(self, self.connectionVariable, "Bluetooth", "WiFi")
        self.connectionMethod.config(bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
        dropDown = self.nametowidget(self.connectionMethod.menuname)
        dropDown.config(bg=self.bgcolour, fg=self.fgcolour, font=self.textstyle)
        
        #Grid management
        self.inventoryLabel.grid(column=0, row=0)
        self.inventoryValue.grid(column=1, row=0)
        self.errorLabel.grid(column=0, row=1)
        self.errorStateValue.grid(column=1, row=1)
        self.inventoryAdjust.grid(column=0, row=2, columnspan=2)
        self.bluetoothLabel.grid(column=3, row=0)
        self.wifiLabel.grid(column=3, row=1)
        self.bluetoothStatus.grid(column=4, row=0)
        self.wifiStatus.grid(column=4, row=1)
        self.connectionMethod.grid(column=3, row=2, columnspan=2)
        self.bluetoothConnect.grid(column=3, row=3)

        #Update values constantly
        self.update_values()

    def update_values(self):
        #Update values after a given time interval in ms
        interval = 100

        #Initialise key and value to be invalid each loop
        key, value = 0, 0

        #Recieve new data via UDP connection
        if (self.connectionVariable.get() == 'Bluetooth'):
            try:
                key, value = self.BTListener.recieve_keyvalue()
            except:
                print('Failed to recieve Bluetooth data')
        elif (self.connectionVariable.get() == 'WiFi'):
            try:
                key, value = self.UDPListener.recieve_keyvalue()
            except:
                print('Failed to recieve data via UDP')
        else:
            print('No valid connection selected')
        
        
        #Handles recieved key value
        self.interpret_keyvalue(key, value)

        #Update inventory value and display
        self.inventoryValue.config(text=str(self.inventory))
        if (self.inventory > 0):
            self.inventoryValue.config(fg='green')
        else:
            self.inventoryValue.config(fg='red')

        #Update Error State and display
        self.errorStateValue.config(text=str(self.errorState))
        if (self.errorState):
            self.errorStateValue.config(fg='red')
        else:
            self.errorStateValue.config(fg='green')

        self.after(interval, self.update_values)

        #Update bluetooth and wifi status indicators
        self.bluetoothStatus.config(text=str(self.bluetoothState))
        if (self.bluetoothState):
            self.bluetoothStatus.config(fg='green')
        else:
            self.bluetoothStatus.config(fg='red')

        self.wifiStatus.config(text=str(self.wifiState))
        if (self.wifiState):
            self.wifiStatus.config(fg='green')
        else:
            self.wifiStatus.config(fg='red')

    #Defined seperate window for adjusting inventory
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
        #self.connection.send_keyvalue(3, value)
        self.top.destroy()
    
    #Interprets key-value pair and performs relevant operations
    def interpret_keyvalue(self, key, value):
        if key == 1: #Key of 1 indicates inventory value
            self.inventory = value
        elif key == 2: #Key of 2 indicates error status
            self.errorState = value
        elif key == 3: #Key of 3 indicates outbound inventory and should be ignored
            print(value)
        else:
            print(f'Invalid key: {key}')

        
if __name__ == '__main__':
    root = tk.Tk()
    TelemetryUI(root).pack()
    root.mainloop()