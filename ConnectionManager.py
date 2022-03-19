class ConnectionManager:
    def __init__(self):
        self.bluetoothStatus = False
        self.wifiStatus = False
    
    def getWifiStatus(self):
        return self.wifiStatus

    def getBluetoothStatus(self):
        return self.bluetoothStatus
    
    def updateBluetoothStatus(self, status):
        self.bluetoothStatus = status
    
    def updateWifiStatus(self, status):
        self.wifiStatus = status