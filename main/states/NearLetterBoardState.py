#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from main.states.GameState import GameState
from main.states.HasReadLetterBoardState import HasReadLetterBoardState
import time
from main.constants import LETTER_POSITION_FOR_GUI

class NearLetterBoardState(GameState):

    def doAction(self):
        print self.nameMyself()
        self.fetchLetterFromLetterBoard()
        
    def fetchLetterFromLetterBoard(self):
        self.game.robot.rotateToAngle(180)
        self.game.robot.setCamMiddle()
        self.game.robot.setCamUp()
        self.game.robot.findLetterInLetterBoard(self.game.getPositionToReadInLetterBoard())
        firstcorner = self.game.robot.findLetterInLetterBoard(self.game.getPositionToReadInLetterBoard())
        if firstcorner == None:
            firstcorner = self.tryDifferentsThingsToReadTheBoard()
        if firstcorner == None:
            print "This is impossible to fetch the letter in the board at position " + str(self.game.getPositionToReadInLetterBoard())
            time.sleep(15)    
        self.game.listOfPucks[0].setCornerToBePlaced(firstcorner)
        self.game.robotQueue.put("LP-" + firstcorner + "-" + LETTER_POSITION_FOR_GUI[self.game.positionToReadInLetterBoard])
        self.game.currentState = HasReadLetterBoardState(self.game)
        
    def tryDifferentsThingsToReadTheBoard(self):
        
        self.game.robot.moveRight(10)
        corner = self.game.robot.findLetterInLetterBoard(self.game.getPositionToReadInLetterBoard())
        self.game.robot.moveLeft(10)
        if corner != None:
            return corner
        
        self.game.robot.moveLeft(10)
        corner = self.game.robot.findLetterInLetterBoard(self.game.getPositionToReadInLetterBoard())
        self.game.robot.moveRight(10)
        if corner != None:
            return corner
        
        self.game.robot.moveForward(25)
        corner = self.game.robot.findLetterInLetterBoard(self.game.getPositionToReadInLetterBoard())
        self.game.robot.backForward(25)
        if corner != None:
            return corner
       
        return None
    
    def nameMyself(self):
        return "NearLetterBoardState"

        
