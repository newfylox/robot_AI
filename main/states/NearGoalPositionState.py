#!/usr/bin/env python
# -*- coding: utf-8 -*-

import HasNoPuckState
from main.states.GameState import GameState
from main.constants import COLOR_OF_PUCKS

class NearGoalPositionState(GameState):

    def doAction(self):
        print self.nameMyself()
        puck = self.game.listOfPucks[self.game.puckNumberBeingProcessed]
        self.goalCorner = puck.getCornerToBePlaced()
        self.rotateToCorrespondingCorner()
        self.goToCorner()
        self.dropPuck()
        
    def rotateToCorrespondingCorner(self):
        if self.goalCorner == "A":
            self.game.robot.rotateToAngle(225)
        elif self.goalCorner == "B":
            self.game.robot.rotateToAngle(130)
        elif self.goalCorner == "C":
            self.game.robot.rotateToAngle(45)
        elif self.goalCorner == "D":
            self.game.robot.rotateToAngle(315)
        
    def goToCorner(self):
        robotDistanceToCorner = self.game.robot.getDistanceToCorner()
        if robotDistanceToCorner == -1:
            print "Error, move the robot because it cannot find the distance"
        else:
            self.game.robot.moveBackward(robotDistanceToCorner)
            
    def dropPuck(self):
            self.game.robot.dropPuck()
            self.game.robot.moveForward(20)
            
            self.game.listOfPucks[self.game.puckNumberBeingProcessed].hasBeenPlaced = True
            colorOfPuckJustBeenPlaced = COLOR_OF_PUCKS[self.game.listOfPucks[self.game.puckNumberBeingProcessed].getPrimaryColor()]
            cornerWhichPuckHasJustBeenPlaced = self.game.listOfPucks[self.game.puckNumberBeingProcessed].getCornerToBePlaced()
            message = "ADDPUCK-" + cornerWhichPuckHasJustBeenPlaced + "-" + str(colorOfPuckJustBeenPlaced)
            self.game.robotQueue.put(message)
            self.game.puckNumberBeingProcessed = self.game.puckNumberBeingProcessed + 1
            self.game.currentState = HasNoPuckState.HasNoPuckState(self.game)
   
    def nameMyself(self):
        return "NearGoalPositionState"
