#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import time
from main.constants import RESET_MINIMUM_NODE

class TrajectoryPlanner:

    def __init__(self, aMap, showSteps):  # @ReservedAssignment
        
        # If TRUE, will print every step of the search    
        self.showSteps = showSteps
        
        # Matrix and its dimension
        self.map = aMap
        self.matrix = aMap.getMatrix()
        self.mapHeight = aMap.mapHeight
        self.mapWidth = aMap.mapWidth

    def getDirections(self, startPositionXY, endPositionXY):      

        # Path finding
        self.path = ""
        
        # Temporary variables used by fonctions
        self._temp_A = 0
        self._temp_B = 0
        self._counter = 0
        
        # Temporary variables when searching for a node with a lower value
        self._minimum_node = 666  # Default value 
                
        self._new_state = 1
        self._old_state = 1
        
        # location of the node with the minimum value
        # 1 = up,   2 = right,   3 = down,   4 = left
        # 5 = upD,   6 = rD,   7 = dD,  8 = lD
        self._min_node_location = 666
        
        # Robot and goal position in the matrix
        self._robot_x, self._robot_y = self.map.translatePositionXYToPositionIJ(startPositionXY)
        self._goal_x, self._goal_y = self.map.translatePositionXYToPositionIJ(endPositionXY)
        
        if (self._robot_x, self._robot_y) == (self._goal_x, self._goal_y):
            return "NOTHINGTODO", []
          
        if self.map.isPositionIJFree(self._robot_x, self._robot_y) == False:
            return "STARTNOTFREE", []
            time.sleep(10)
            
        if self.map.isPositionIJFree(self._goal_x, self._goal_y) == False:
            print "THE GOAL POSITION OF THE ROBOT IS NOT FREE"
            return 0,0
        
        self.pathWithRobotPosition = []
        self.pathWithIJPosition = []
        self.pathWithCardinalDirections = []
        
        while self.matrix[self._robot_x][self._robot_y] != self._goal:
            # find new location the robot should go to
            self._new_state = self.propagateWavefront()
            # update location of the robot
            if self._new_state == 1:
                self._robot_x -= 1
                if self.showSteps:
                    print "Move to x = %d and  y = %d\n\n" % \
                        (self._robot_x, self._robot_y)
                self.pathWithRobotPosition.append((self._robot_x, self._robot_y))
                self.pathWithCardinalDirections.append("N")
                tempString = str(self._robot_x)+","+str(self._robot_y)
                self.pathWithIJPosition.append(tempString)
                
            if self._new_state == 2:
                self._robot_x -= 1
                self._robot_y += 1
                if self.showSteps:
                    print "Robot is moving to x = %d and y = %d\n\n" % \
                        (self._robot_x, self._robot_y)
                self.pathWithRobotPosition.append((self._robot_x, self._robot_y))
                self.pathWithCardinalDirections.append("NE")
                tempString = str(self._robot_x)+","+str(self._robot_y)
                self.pathWithIJPosition.append(tempString)
                
            if self._new_state == 3:
                self._robot_y += 1
                if self.showSteps:
                    print "Robot is moving to x = %d and y = %d\n\n" % \
                        (self._robot_x, self._robot_y)
                self.pathWithRobotPosition.append((self._robot_x, self._robot_y))
                self.pathWithCardinalDirections.append("E")
                tempString = str(self._robot_x)+","+str(self._robot_y)
                self.pathWithIJPosition.append(tempString)
                
            if self._new_state == 4:
                self._robot_x += 1
                self._robot_y += 1
                if self.showSteps:
                    print "Robot is moving to x = %d and y = %d\n\n" % \
                        (self._robot_x, self._robot_y)
                self.pathWithRobotPosition.append((self._robot_x, self._robot_y))
                self.pathWithCardinalDirections.append("SE")
                tempString = str(self._robot_x)+","+str(self._robot_y)
                self.pathWithIJPosition.append(tempString)
                
            if self._new_state == 5:
                self._robot_x += 1
                if self.showSteps:
                    print "Robot is moving to x = %d and y = %d\n\n" % \
                        (self._robot_x, self._robot_y)
                self.pathWithRobotPosition.append((self._robot_x, self._robot_y))
                self.pathWithCardinalDirections.append("S")
                tempString = str(self._robot_x)+","+str(self._robot_y)
                self.pathWithIJPosition.append(tempString)                
                
            if self._new_state == 6:
                self._robot_x += 1
                self._robot_y -= 1
                if self.showSteps:
                    print "Robot is moving to x = %d and y = %d\n\n" % \
                        (self._robot_x, self._robot_y)
                self.pathWithRobotPosition.append((self._robot_x, self._robot_y))
                self.pathWithCardinalDirections.append("SO")
                tempString = str(self._robot_x)+","+str(self._robot_y)
                self.pathWithIJPosition.append(tempString)
                
            if self._new_state == 7:
                self._robot_y -= 1
                if self.showSteps:
                    print "Robot is moving to x = %d and y = %d\n\n" % \
                        (self._robot_x, self._robot_y)
                self.pathWithRobotPosition.append((self._robot_x, self._robot_y))   
                self.pathWithCardinalDirections.append("O")
                tempString = str(self._robot_x)+","+str(self._robot_y)
                self.pathWithIJPosition.append(tempString) 
                
            if self._new_state == 8:
                self._robot_x -= 1
                self._robot_y -= 1
                if self.showSteps:
                    print "Robot is moving to x = %d and y = %d\n\n" % \
                        (self._robot_x, self._robot_y)
                self.pathWithRobotPosition.append((self._robot_x, self._robot_y))    
                self.pathWithCardinalDirections.append("NO")
                tempString = str(self._robot_x)+","+str(self._robot_y)
                self.pathWithIJPosition.append(tempString)
                
            self._old_state = self._new_state
            
        msg = "Map size = %i x %i\n\n" % (self.mapHeight, self.mapWidth)
        if self.showSteps:
            print msg
            self.printMap()
        return self.groupDirectionsInPath(self.pathWithCardinalDirections)

    def propagateWavefront(self):

        self.clearPropagation()
        # Old robot location was deleted, store new robot location in matrix
        self.matrix[self._robot_x][self._robot_y] = self._robot
        self.path = self._robot
        # getDirections location to begin scan at goal location
        self.matrix[self._goal_x][self._goal_y] = self._goal
        counter = 0
        while counter < 200:  # buffer ...
            x = 0
            y = 0
            # while the matrix hasnt been fully scanned
            while x < self.mapHeight and y < self.mapWidth:
                # ignore if its an obstacle or the goal
                if self.matrix[x][y] != self._obstacle and \
                    self.matrix[x][y] != self._goal:
                    #Path found !!!
                    minLoc = self.minimumSurroundingNodeValue(x, y)
                    if minLoc < self._reset_min and \
                        self.matrix[x][y] == self._robot:
                        if self.showSteps:
                            print "The Wavefront is finished:\n"
                            self.printMap()
                        # Tell the robot to move after this return.
                        return self._min_node_location
                    # record a value in to this node
                    elif self._minimum_node != self._reset_min:
                        # if this isnt here, 'nothing' will go in the location
                        self.matrix[x][y] = self._minimum_node + 1
                # go to next node and/or row
                y += 1
                if y == self.mapWidth and x != self.mapHeight:
                    x += 1
                    y = 0
            # print self._robot_x, self._robot_y
            if self.showSteps:
                print "Sweep # %i\n" % (counter + 1)
                self.printMap()
            counter += 1
        return 0
    

    def clearPropagation(self):
        for x in range(0, self.mapHeight):
            for y in range(0, self.mapWidth):
                if self.matrix[x][y] != self._obstacle and self.matrix[x][y] != self._goal and \
                    self.matrix[x][y] != self.path:
                    self.matrix[x][y] = self._nothing 
                    
    def clearMap(self):
        for x in range(0, self.mapHeight):
            for y in range(0, self.mapWidth):
                if self.matrix[x][y] != self._obstacle: 
                    self.matrix[x][y] = self._nothing 

    def minimumSurroundingNodeValue(self, x, y):
        
        "minimumSurroundingNodeValue looks at a node at the" 
        "position given and returns the lowest value around that node"

        # reset minimum
        self._minimum_node = RESET_MINIMUM_NODE
        
        # down if the not last, check before it
        if x < self.mapHeight - 1:
            if self.matrix[x + 1][y] < self._minimum_node and \
                self.matrix[x + 1][y] != self._nothing:
                # find the lowest number node, and exclude empty nodes (0's)
                self._minimum_node = self.matrix[x + 1][y]
                self._min_node_location = 5
                
        # up if the not first, check before it
        if x > 0:
            if self.matrix[x - 1][y] < self._minimum_node and \
                self.matrix[x - 1][y] != self._nothing:
                self._minimum_node = self.matrix[x - 1][y]
                self._min_node_location = 1
                
        # right if the not first, check before it
        if y < self.mapWidth - 1:
            if self.matrix[x][y + 1] < self._minimum_node and \
                self.matrix[x][y + 1] != self._nothing:
                self._minimum_node = self.matrix[x][y + 1]
                self._min_node_location = 3
                
        # left if the not first, check before it
        if y > 0: 
            if self.matrix[x][y - 1] < self._minimum_node and \
                self.matrix[x][y - 1] != self._nothing:
                self._minimum_node = self.matrix[x][y - 1]
                self._min_node_location = 7
                  
        # up-left diagonal
        if x > 0  and y > 0: 
            if self.matrix[x - 1][y - 1] < self._minimum_node and \
                self.matrix[x - 1][y - 1] != self._nothing:
                self._minimum_node = self.matrix[x - 1][y - 1]
                self._min_node_location = 8
                
        # up-right diagonal  
        if x > 0  and y < self.mapWidth - 1: 
            if self.matrix[x - 1][y + 1] < self._minimum_node and \
                self.matrix[x - 1][y + 1] != self._nothing:
                self._minimum_node = self.matrix[x - 1][y + 1]
                self._min_node_location = 2
                 
        # down-left diagonal
        if x < self.mapHeight - 1  and y > 0: 
            if self.matrix[x + 1][y - 1] < self._minimum_node and \
                self.matrix[x + 1][y - 1] != self._nothing:
                self._minimum_node = self.matrix[x + 1][y - 1]
                self._min_node_location = 6
                
        # down-right diagonal
        if x < self.mapHeight - 1  and y < self.mapWidth - 1: 
            if self.matrix[x + 1][y + 1] < self._minimum_node and \
                self.matrix[x + 1][y + 1] != self._nothing:
                self._minimum_node = self.matrix[x + 1][y + 1]
                self._min_node_location = 4
                
        return self._minimum_node

    def printMap(self):
        lign = ''
        for temp_B in range(0, self.mapHeight):
            for temp_A in range(0, self.mapWidth):
                if self.matrix[temp_B][temp_A] == self._obstacle:
                    lign += "%4s" % "[X]"
                elif self.matrix[temp_B][temp_A] == self._robot:
                    lign += "%4s" % "-"
                elif self.matrix[temp_B][temp_A] == self._goal:
                    lign += "%4s" % "G"
                else:
                    lign += "%4s" % str(self.matrix[temp_B][temp_A])
            lign += "\n\n"
        lign += "\n\n"
        print lign
        
    def groupDirectionsInPath(self, aList):
        indice = 0
        finalList = []
        finalStringList = ""
        
        numberOfRepetitions = 1

        while (indice < len(aList)):
            element = aList[indice]
            while indice + 1 < len(aList) and aList[indice + 1] == element:
                    numberOfRepetitions = numberOfRepetitions + 1
                    indice = indice + 1
                  
            finalStringList = finalStringList + str(str(numberOfRepetitions) + "*" + element)
            finalStringList = finalStringList + "-" 
            finalList.append(str(str(numberOfRepetitions) + "*" + element))
            indice = indice + 1
            numberOfRepetitions = 1
                
        return finalStringList, self.pathWithIJPosition
