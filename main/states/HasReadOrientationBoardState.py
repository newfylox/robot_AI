#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from main.states.GameState import GameState
from main.states.NearPucksState import NearPucksState
from main.constants import COLOR_OF_PUCKS

class HasReadOrientationBoardState(GameState):

    def doAction(self):
        print self.nameMyself()
        self.findCorrespondingCornersToPucks()
        self.resetPuckListAccordingToPlacindPriority()
        self.goNearPucks()
    
    def findCorrespondingCornersToPucks(self):

        if self.game.getPucksOrientation() == "SH":
            if self.game.listOfPucks[0].cornerToBePlaced == "A":
                self.game.listOfPucks[1].setCornerToBePlaced("B")
                self.game.listOfPucks[2].setCornerToBePlaced("C")
                
            if self.game.listOfPucks[0].cornerToBePlaced == "B":
                self.game.listOfPucks[1].setCornerToBePlaced("C")
                self.game.listOfPucks[2].setCornerToBePlaced("D")
                
            if self.game.listOfPucks[0].cornerToBePlaced == "C":
                self.game.listOfPucks[1].setCornerToBePlaced("D")
                self.game.listOfPucks[2].setCornerToBePlaced("A")
                
            if self.game.listOfPucks[0].cornerToBePlaced == "D":
                self.game.listOfPucks[1].setCornerToBePlaced("A")
                self.game.listOfPucks[2].setCornerToBePlaced("B")          
        elif self.game.getPucksOrientation() == "SA":
            if self.game.listOfPucks[0].cornerToBePlaced == "A":
                self.game.listOfPucks[1].setCornerToBePlaced("D")
                self.game.listOfPucks[2].setCornerToBePlaced("C")
                
            if self.game.listOfPucks[0].cornerToBePlaced == "B":
                self.game.listOfPucks[1].setCornerToBePlaced("A")
                self.game.listOfPucks[2].setCornerToBePlaced("D")
                
            if self.game.listOfPucks[0].cornerToBePlaced == "C":
                self.game.listOfPucks[1].setCornerToBePlaced("B")
                self.game.listOfPucks[2].setCornerToBePlaced("A")
                
            if self.game.listOfPucks[0].cornerToBePlaced == "D":
                self.game.listOfPucks[1].setCornerToBePlaced("C")
                self.game.listOfPucks[2].setCornerToBePlaced("B")
                
        self.game.robotQueue.put(self.game.listOfPucks[0].getCornerToBePlaced() + "-" + COLOR_OF_PUCKS[self.game.listOfPucks[0].getPrimaryColor()])
        self.game.robotQueue.put(self.game.listOfPucks[1].getCornerToBePlaced() + "-" + COLOR_OF_PUCKS[self.game.listOfPucks[1].getPrimaryColor()])
        self.game.robotQueue.put(self.game.listOfPucks[2].getCornerToBePlaced() + "-" + COLOR_OF_PUCKS[self.game.listOfPucks[2].getPrimaryColor()])

    def resetPuckListAccordingToPlacindPriority(self):
        
        #Rearrange the list accoring to priority puck   
        newListOfPuck =[]      
        for puck in self.game.listOfPucks:
            if puck.priority == 1:
                newListOfPuck.append(puck)
                
        for puck in self.game.listOfPucks:
            if puck.priority == 2:
                newListOfPuck.append(puck)
                
        self.game.listOfPucks = newListOfPuck
    
    def goNearPucks(self):
        self.game.robot.moveRight(20)   
        self.game.currentState = NearPucksState(self.game)
    
    def nameMyself(self):
        return "HasReadOrientationBoardState"

