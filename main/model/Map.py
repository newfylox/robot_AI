from math import ceil
import numpy
from main.constants import OBSTACLE, ROBOT, GOAL, NOTHING,\
    CELL_EXPAND_CENTIMETER, WALL_EXPAND_CENTIMETER, WIDHT_TABLE, LENGHT_TABLE,\
    EXPAND, PUCK_EXPAND_CENTIMETER, PUCK
from main.model.Position import Position

class Map(object):

    def __init__(self, cellDimension):
        self.cellDimension = cellDimension
        self.numberOfCellsToExpandForObstacles = int(ceil(CELL_EXPAND_CENTIMETER / self.cellDimension))
        self.numberOfCellsToExpandForPucks = int(ceil(PUCK_EXPAND_CENTIMETER / self.cellDimension))
        self.numberOfCellsToExpandForWall = int(ceil(WALL_EXPAND_CENTIMETER / self.cellDimension))        
        self.numberOfHorizontalCells = 0
        self.numberOfVerticalCells = 0
        self.matrix = [0]
        
        # Creation of the map in the matrix
        self.createMap()
        
    def getCellDimension(self):
        return self.cellDimension        
        
    def getMatrix(self):
        return self.matrix
    
    def createMap(self):
        self.numberOfHorizontalCells = int(ceil(WIDHT_TABLE / self.cellDimension))
        self.numberOfVerticalCells = int(ceil(LENGHT_TABLE / self.cellDimension))      
        
        self.temp_A = 0
        self.temp_B = 0
        
        self.matrix = numpy.zeros(self.numberOfHorizontalCells * self.numberOfVerticalCells, dtype=numpy.int).reshape((self.numberOfVerticalCells, self.numberOfHorizontalCells))
        self.mapHeight, self.mapWidth = self.matrix.shape
  
        self.expandWalls()

    def expandWalls(self):        
        # For the first ligns
        for i in range(0, self.numberOfCellsToExpandForWall):
            for j in range(0, self.mapWidth):
                self.matrix[i][j] = 999
                  
        # For the first rows
        for i in range(self.mapHeight - self.numberOfCellsToExpandForWall, self.mapHeight):
            for j in range(0, self.mapWidth):
                self.matrix[i][j] = 999
                
        # For the last ligns
        for i in range(0, self.mapHeight):
            for j in range(0, self.numberOfCellsToExpandForWall):
                self.matrix[i][j] = 999
                
        # For the last rows
        for i in range(0, self.mapHeight):
            for j in range(self.mapWidth - self.numberOfCellsToExpandForWall, self.mapWidth):
                self.matrix[i][j] = 999
        
    def expandObstacle(self, obstacleI, obstacleJ):
        # Plus one because the range exclude the last number
        for i in range(obstacleI - self.numberOfCellsToExpandForObstacles, obstacleI + self.numberOfCellsToExpandForObstacles + 1):
            for j in range(obstacleJ - self.numberOfCellsToExpandForObstacles, obstacleJ + self.numberOfCellsToExpandForObstacles + 1):
                if i > -1 and j > -1 and i < self.numberOfVerticalCells and j < self.numberOfHorizontalCells:
                    self.matrix[i][j] = 999
        self.matrix[obstacleI][obstacleJ] = 9999    
        
    def expandPuck(self, puckCornerI, puckCornerJ):
        # Plus one because the range exclude the last number
        for i in range(puckCornerI - self.numberOfCellsToExpandForPucks, puckCornerI + self.numberOfCellsToExpandForPucks + 1):
            for j in range(puckCornerJ - self.numberOfCellsToExpandForPucks, puckCornerJ + self.numberOfCellsToExpandForPucks + 1):
                if i > -1 and j > -1 and i < self.numberOfVerticalCells and j < self.numberOfHorizontalCells:
                    self.matrix[i][j] = 999
        self.matrix[puckCornerI][puckCornerJ] = 9998   
        
        
    def printMap(self):
        lign = ''
        for temp_B in range(0, self.mapHeight):
            for temp_A in range(0, self.mapWidth):
                if self.matrix[temp_B][temp_A] == OBSTACLE:
                    lign += "%4s" % "[X]"
                elif self.matrix[temp_B][temp_A] == PUCK:
                    lign += "%4s" % "P"
                elif self.matrix[temp_B][temp_A] == EXPAND:
                    lign += "%4s" % "x"
                elif self.matrix[temp_B][temp_A] == ROBOT:
                    lign += "%4s" % "R"
                elif self.matrix[temp_B][temp_A] == GOAL:
                    lign += "%4s" % "G"
                else:
                    lign += "%4s" % str(self.matrix[temp_B][temp_A])
            lign += "\n\n"
        lign += "\n\n"
        print lign
         
    def addObstacle(self, obstaclePosition):  
        obstaclePosition_I, obstaclePosition_J = self.translatePositionXYToPositionIJ(obstaclePosition)
        self.expandObstacle(obstaclePosition_I, obstaclePosition_J)
        
    def addPuck(self, corner):          
        positionXCorner = 0
        positionYCorner = 0
        if corner == "A":
            positionXCorner, positionYCorner = 87, 87
        elif corner == "B":
            positionXCorner, positionYCorner = 87, 24
        elif corner == "C":
            positionXCorner, positionYCorner = 24, 24
        elif corner == "D":
            positionXCorner, positionYCorner = 24, 87
            
        puckCornerPosition = Position(positionXCorner, positionYCorner)
        
        puckCorner_I, puckCorner_J = self.translatePositionXYToPositionIJ(puckCornerPosition)
        
        self.expandPuck(puckCorner_I, puckCorner_J)
                            
    def translatePositionXYToPositionIJ(self, position):
        posX = int(position.getX())
        posY = int(position.getY())
        
        # Temporary variables for calculations
        tempIndex_i = 0
        tempIndex_j = 0
        temp_i_Balayage = 0
        temp_j_Balayage = 0     
        posI = -1
        posJ = -1

        while tempIndex_i in range(0, self.mapHeight):
            if posX >= temp_i_Balayage and posX < (temp_i_Balayage + self.cellDimension):
                posI = tempIndex_i
            temp_i_Balayage = temp_i_Balayage + self.cellDimension
            tempIndex_i = tempIndex_i + 1
            
        while tempIndex_j in range(0, self.mapWidth):
            if posY >= temp_j_Balayage and posY < temp_j_Balayage + self.cellDimension:
                posJ = tempIndex_j
            temp_j_Balayage = temp_j_Balayage + self.cellDimension
            tempIndex_j = tempIndex_j + 1
            
        return (posI, posJ)
    
    def isPositionXYFree(self, position):
        positionI, positionJ = self.translatePositionXYToPositionIJ(position)
        return self.matrix[positionI][positionJ] == NOTHING
    
    def isPositionIJFree(self, positionI, positionJ):
        return self.matrix[positionI][positionJ] == NOTHING
