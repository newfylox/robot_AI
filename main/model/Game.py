#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from main.states.NoResistanceValueState import NoResistanceValueState

class Game(object):
    
    def __init__(self, robot, queue):
        self.robotQueue = queue
        self.robot = robot
        self.currentState = NoResistanceValueState(self)        
        self.isKilled = False
        self.listOfPucks = []
        self.puckNumberBeingProcessed = 0
        self.positionToReadInLetterBoard = -1
        self.positionToReadInOrientationBoard = -1
        self.resistanceValue = -1
        self.pucksOrientation = ""
        self.status = "Stopped"
        self.obstaclesFound = False
        
    def doAction(self):
        self.currentState.doAction() 
        
    def isInProcess(self):
        return self.status == "Started"

    def start(self):
        self.status = "Started"
        self.robotQueue.put("STARTRECEIVED")
        
    def stop(self):
        self.status = "Stopped"   
   
    def getCurrentStateName(self):
        return self.currentState.nameMyself()   

    def setResistanceValue(self, newResistanceValue):
        self.resistanceValue = newResistanceValue

    def getResistanceValue(self):
        return self.resistanceValue

    def setPuckNumberBeingProcessed(self, newNumber):
        self.puckNumberBeingProcessed = newNumber

    def getPuckNumberBeingProcessed(self):
        return self.puckNumberBeingProcessed

    def setPositionToReadInLetterBoard(self, newPosition):
        self.positionToReadInLetterBoard = newPosition

    def getPositionToReadInLetterBoard(self):
        return self.positionToReadInLetterBoard
    
    def setPositionToReadInOrientationBoard(self, newPosition):
        self.positionToReadInOrientationBoard = newPosition    

    def getPositionToReadInOrientationBoard(self):
        return self.positionToReadInOrientationBoard
    
    def setPucksOrientation(self, newOrientation):
        self.pucksOrientation = newOrientation
        
    def getPucksOrientation(self):
        return self.pucksOrientation        
      
    def isFinished(self):
        return self.getNumberOfPucksPlaced() >=3
    
    def getNumberOfPucksPlaced(self):
        numberOfPucksPlaced = 0
        for puck in self.listOfPucks:
            if puck.hasBeenPlaced == True:
                numberOfPucksPlaced = numberOfPucksPlaced + 1
        return numberOfPucksPlaced 

    def reset(self):
        self.currentState = NoResistanceValueState(self)        
        self.isKilled = False
        self.listOfPucks = []
        self.puckNumberBeingProcessed = 0
        self.positionToReadInLetterBoard = -1
        self.positionToReadInOrientationBoard = -1
        self.resistanceValue = -1
        self.pucksOrientation = ""
        self.status = "Stopped"
        self.obstaclesFound = False
        
