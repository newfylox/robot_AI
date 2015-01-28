class Position(object):

    def __init__(self, positionX, positionY):
        if type(positionX) is str:
            self.X = float(positionX)
            self.Y = float(positionY)
        else:
            self.X = float(positionX)
            self.Y = float(positionY)     
    
    def getX(self):
        return (self.X)
    
    def getY(self):
        return (self.Y)
         
    def toString(self):
        return "(" + str(self.X) + ", " + str(self.Y) + ")"    
        