from random import randint

class TelemetryData():
    def __init__(self):
        self.Inventory = 0
        self.ErrorState = False

    def increase(self):
        self.Inventory += 1
    
    def decrease(self):
        self.Inventory -= 1

    def getInventory(self):
        return int(self.Inventory)

    def getErrorState(self):
        return bool(self.ErrorState) 
    
    def updateValues(self):
        #TODO - Will eventually be used to update inventory and error state values using data from unit
        pass

