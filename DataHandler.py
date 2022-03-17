from random import randint

class TelemetryData():
    def __init__(self):
        self.Inventory = 0
        self.ErrorState = False

    def getInventory(self):
        return randint(0, 100)

    def getErrorState(self):
        return self.ErrorState    

