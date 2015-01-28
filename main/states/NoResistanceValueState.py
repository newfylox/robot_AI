#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from main.states.GameState import GameState
from main.states.NearResistanceState import NearResistanceState
from main.model.Position import Position
POSITION_TO_GO_FOR_RESISTANCE_TRAY_ = Position(30,30)

class NoResistanceValueState(GameState):

    def doAction(self):
        print self.nameMyself()  
        self.goNextToResistanceTray()
    
    def goNextToResistanceTray(self):      
        self.game.robot.refreshPositionAndAngle()
        self.game.robot.rotateToAngle(0)
        self.game.robot.rotateToAngle(0)
        xDifference = self.game.robot.position.getX() - 23
        yDifference = self.game.robot.position.getY() - 8
        self.game.robot.moveBackward(xDifference)
        self.game.robot.moveRight(yDifference)
        self.game.currentState = NearResistanceState(self.game)        
        
    def nameMyself(self):
        return "NoResistanceValueState"
    

