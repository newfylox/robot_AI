#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from main.states.GameState import GameState
from main.states.NearGoalPositionState import NearGoalPositionState
from main.constants import POSITION_TO_GO_MID_SQUARE

class HasPuckState(GameState):

    def doAction(self):
        print self.nameMyself()
        self.fetchGoalPosition()
        
    def fetchGoalPosition(self):
        self.game.robot.moveToPosition(POSITION_TO_GO_MID_SQUARE)
        self.game.currentState = NearGoalPositionState(self.game) 
        
    def nameMyself(self):
        return "HasPuckState"
