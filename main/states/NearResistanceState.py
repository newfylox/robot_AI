#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from main.states.GameState import GameState
from main.states.HasReadResistanceState import HasReadResistanceState
import time
from main.constants import WIDHT_TABLE

class NearResistanceState(GameState):

    def doAction(self):
        print self.nameMyself()
        self.resistanceValue = 5000
        self.fetchResistance()
        self.goHide()
        self.requestObstaclesPositions()
        self.stopHiding()
        
    def fetchResistance(self):                     
        while float(self.resistanceValue) > 4200:
            tempValue = self.game.robot.readResistance() 
            if tempValue != None :
                self.resistanceValue = tempValue
        
        self.game.resistanceValue = self.resistanceValue
        self.game.robotQueue.put("RV-" + str(self.game.resistanceValue))  
        self.game.robot.moveLeft(30)
        self.game.robot.moveForward(30)
        
    def goHide(self):
        self.game.robot.refreshPositionAndAngle()
        self.game.robot.rotateToAngle(0)
        xPosition = self.game.robot.position.getX()
        yPosition = self.game.robot.position.getY()
        self.game.robot.moveBackward(xPosition - 27)
        self.game.robot.moveLeft(WIDHT_TABLE - yPosition - 23)

    def requestObstaclesPositions(self):       
        self.game.robotQueue.put("REQUESTOBSTACLES")
        while self.game.robot.obstaclesPositionFetched == False:
            time.sleep(1)
            
    def stopHiding(self):
        self.game.robot.moveRight(30)
        self.game.robot.moveForward(30)        
        self.game.currentState = HasReadResistanceState(self.game)
        
    def nameMyself(self):
        return "NearResistanceState"
