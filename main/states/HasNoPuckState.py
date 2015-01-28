#!/usr/bin/env python
# -*- coding: utf-8 -*-

import NearPucksState
from main.states.GameState import GameState
from main.constants import POSITION_TO_GO_MID_PUCKS

class HasNoPuckState(GameState):

    def doAction(self):
        print self.nameMyself()
        
        if self.game.isFinished():
            print "The game is Finished !"
            self.game.stop()
            self.game.robotQueue.put("GAMEFINISHED")
            self.game.robot.setLedOn()
        else:
            self.game.robot.moveToPosition(POSITION_TO_GO_MID_PUCKS)
            self.game.currentState = NearPucksState.NearPucksState(self.game)
        
    def nameMyself(self):
        return "HasNoPuckState"

         

        
    

        
