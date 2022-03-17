from random import randint

class TelemetryData():
    def __init__(self):
        self.Inventory = 0
        self.ErrorState = False

    def getInventory(self):
        return self.Inventory

    def getErrorState(self):
        return self.ErrorState    
    
    def updateValues(self):
        #TODO - Will eventually be used to update inventory and error state values using data from unit
        pass

