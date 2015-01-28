#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from main.model.Puck import Puck
from main.states.GameState import GameState
from main.states.NearLetterBoardState import NearLetterBoardState
from main.constants import POSITION_FACING_LETTER_BOARD, COLOR_OF_PUCKS

class HasReadResistanceState(GameState):

    def doAction(self):
        print self.nameMyself()
        number1, number2, number3 = self.splitResistanceValueInThreeNumbers(self.game.resistanceValue)
        self.findCorrespondingPositionToReadInBoards(int(number1), int(number3))
        self.findCorrespondingColorsOfPucks(int(number1), int(number2), int(number3))
        self.goNextToLetterBoard()

    def splitResistanceValueInThreeNumbers(self, resistanceValue):
        factorValue = len(str(resistanceValue))
        resistanceValue = float(resistanceValue)
        resistanceValue = str(round(resistanceValue, 5-factorValue)*1000)
        return resistanceValue[0], resistanceValue[1], str(len(resistanceValue)-4)
    
    def findCorrespondingPositionToReadInBoards(self, position1, position2):
        self.game.setPositionToReadInLetterBoard(position1)
        self.game.setPositionToReadInOrientationBoard(position2)
    
    def findCorrespondingColorsOfPucks(self, number1, number2, number3):
        
        #Because the first and third number of the resistance are the most
        #likely to be right so we want to place them first
        puck1 = Puck(number1)
        puck1.setPriority(1)
        puck2 = Puck(number2)
        puck2.setPriority(2)
        puck3 = Puck(number3)
        puck3.setPriority(1)
        
        self.game.listOfPucks.append(puck1)
        self.game.listOfPucks.append(puck2)
        self.game.listOfPucks.append(puck3)
        
        self.game.robotQueue.put("C1-" + COLOR_OF_PUCKS[number1])
        self.game.robotQueue.put("C2-" + COLOR_OF_PUCKS[number2])
        self.game.robotQueue.put("C3-" + COLOR_OF_PUCKS[number3])
        
    def goNextToLetterBoard(self):
        self.game.robot.moveToPosition(POSITION_FACING_LETTER_BOARD)
        self.game.robot.rotateToAngle(180)
        self.game.currentState = NearLetterBoardState(self.game)
