class Puck(object):

    def __init__(self, primaryColorCode):
        self.primaryColor = primaryColorCode
        self.cornerToBePlaced = ""
        self.hasBeenPlaced = False
        self.priority = -1
        
    def setPrimaryColor(self):
        return (self.primaryColor)
    
    def getPrimaryColor(self):
        return (self.primaryColor)
    
    def setCornerToBePlaced(self, letter):
        self.cornerToBePlaced = letter
        
    def getCornerToBePlaced(self):
        return self.cornerToBePlaced

    def setHasBeenPlaced(self, hasBeenPlaced):
        self.hasBeenPlaced = hasBeenPlaced
    
    def hasBeenPlaced(self):
        return self.hasBeenPlaced
    
    def setPriority(self, newPriority):
        self.priority = newPriority
        
    def getPriority(self):
        return self.priority
