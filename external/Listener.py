import redis
import time

HOST = '' #IP address of rasberry pi
PORT = 6379

class Listener():
    def __init__(self):
        self.bluetoothStatus = False
        self.wifiStatus = False
        
        #Connect to redis server
        self.r = redis.Redis(HOST, PORT)

    #Recieves and returns latest inventory reading
    def updateInventory(self):
        return self.r.get("inventory")

    #Revieves and returns current error state
    def updateErrorState(self):
        return self.r.get("error")
    
    #Searches redis for data under provided 'label'
    def receive(self, label):
        return self.r.get("label")

    def getWifiStatus(self):
        return self.wifiStatus

    def getBluetoothStatus(self):
        return self.bluetoothStatus
    
    def updateBluetoothStatus(self, status):
        self.bluetoothStatus = status
    
    def updateWifiStatus(self, status):
        self.wifiStatus = status



