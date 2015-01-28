#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from main.states.GameState import GameState
from main.states.NearOrientationBoardState import NearOrientationBoardState

class HasReadLetterBoardState(GameState):

    def doAction(self):
        print self.nameMyself()
        self.goNextToOrientationBoard()
        
    def goNextToOrientationBoard(self):
        self.game.robot.moveLeft(30)
        self.game.robot.rotateToAngle(180)
        self.game.currentState = NearOrientationBoardState(self.game) 
        
    def nameMyself(self):
        return "HasReadLetterBoardState"
