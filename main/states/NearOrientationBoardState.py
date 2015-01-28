#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import time
from main.states.GameState import GameState
from main.states.HasReadOrientationBoardState import HasReadOrientationBoardState
from main.constants import ORIENTATION_POSITION_FOR_GUI

class NearOrientationBoardState(GameState):

    def doAction(self):
        print self.nameMyself()
        self.fetchOrientationFromOrientationBoard()
        
    def fetchOrientationFromOrientationBoard(self):

        self.game.robot.findOrientationInOrientationBoard(self.game.positionToReadInOrientationBoard)
        self.orientation = self.game.robot.findOrientationInOrientationBoard(self.game.positionToReadInOrientationBoard)
        
        if self.orientation == None:
            self.orientation = self.tryDifferentsThingsToReadTheBoard()
        if self.orientation == None:
            print "This is impossible to fetch the orientation in the board at position " + str(self.game.positionToReadInOrientationBoard())
            time.sleep(15) 

        self.game.setPucksOrientation(self.orientation)
        self.game.robotQueue.put("OP-" + self.game.pucksOrientation + "-" + ORIENTATION_POSITION_FOR_GUI[self.game.positionToReadInOrientationBoard])
        self.game.currentState = HasReadOrientationBoardState(self.game)        

    def tryDifferentsThingsToReadTheBoard(self):
        
        self.game.robot.moveRight(10)
        self.orientation = self.game.robot.findOrientationInOrientationBoard(self.game.getPositionToReadInOrientationBoard())
        self.game.robot.moveLeft(10)
        if self.orientation != None:
            return self.orientation
        
        self.game.robot.moveLeft(10)
        self.orientation = self.game.robot.findOrientationInOrientationBoard(self.game.getPositionToReadInOrientationBoard())
        self.game.robot.moveRight(10)
        if self.orientation != None:
            return self.orientation
        
        self.game.robot.moveForward(25)
        self.orientation = self.game.robot.findOrientationInOrientationBoard(self.game.getPositionToReadInOrientationBoard())
        self.game.robot.BackForward(25)
        if self.orientation != None:
            return self.orientation
       
        return None
        
    def nameMyself(self):
        return "NearOrientationBoardState"
         

