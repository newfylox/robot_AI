#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from main.states.GameState import GameState
from main.states.HasPuckState import HasPuckState
from main.constants import STARTING_ANGLE_FACING_PUCKS



class NearPucksState(GameState):

    def doAction(self):
        print self.nameMyself()
        self.fetchPuck()
        
    def fetchPuck(self):

        self.game.robot.rotateToAngle(STARTING_ANGLE_FACING_PUCKS)       
        self.game.robot.setCamMiddle()
        self.game.robot.setCamDown()

        #Scan the area to search the right puck        
        rotationAngleNeeded, robotDistanceToPuck = self.infiniteScan(30)
                      
        if rotationAngleNeeded > 0:
            self.game.robot.rotateClockwise(rotationAngleNeeded)
        else:
            self.game.robot.rotateCounterClockwise(rotationAngleNeeded)
        
        if self.verifyASecondTimeIfStillSeePuck() == True:
            self.game.robot.moveBackward(robotDistanceToPuck) 
            self.game.robot.grabPuck()
            self.game.robot.moveForward(robotDistanceToPuck)     
            self.game.currentState = HasPuckState(self.game)
        else : 
            self.game.robot.rotateToAngle(STARTING_ANGLE_FACING_PUCKS)
            rotationAngleNeeded, robotDistanceToPuck = self.infiniteScan(20) 
            
            if rotationAngleNeeded > 0:
                self.game.robot.rotateClockwise(rotationAngleNeeded)
            else:
                self.game.robot.rotateCounterClockwise(rotationAngleNeeded)
                
            self.game.robot.moveBackward(robotDistanceToPuck) 
            self.game.robot.grabPuck()
            self.game.robot.moveForward(robotDistanceToPuck)     
            self.game.currentState = HasPuckState(self.game)


    
    def infiniteScan(self, angleNumber):

        puck = self.game.listOfPucks[self.game.puckNumberBeingProcessed]

        puckColorCodeToFind = puck.getPrimaryColor()
        returnedValue1, returnedValue2 = self.game.robot.getDistanceToPuck(puckColorCodeToFind)          
        totalAngle = 0
        while returnedValue1 == -1 and returnedValue2 == -1:
            if totalAngle < 200:
                self.game.robot.rotateCounterClockwise(angleNumber)
                returnedValue1, returnedValue2 = self.game.robot.getDistanceToPuck(puckColorCodeToFind)
            if totalAngle >= 200:
                self.game.robot.rotateClockwise(angleNumber)
                returnedValue1, returnedValue2 = self.game.robot.getDistanceToPuck(puckColorCodeToFind)
            if totalAngle > 390 :
                totalAngle = 0
            totalAngle = totalAngle + angleNumber
            
        return returnedValue1, returnedValue2
                
    def verifyASecondTimeIfStillSeePuck(self):
        
        puckColorCodeToFind = self.game.listOfPucks[self.game.puckNumberBeingProcessed].getPrimaryColor()
        returnedValue1, returnedValue2 = self.game.robot.getDistanceToPuck(puckColorCodeToFind)          
        if returnedValue1 == -1 and returnedValue2 == -1:
            return False
        else:
            return True        
                            
                
    def nameMyself(self):
        return "NearPucksState"
