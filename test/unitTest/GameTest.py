#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
import unittest
from main.model.Robot import Robot
import Queue
from main.model.Game import Game
from main.model.Puck import Puck

RANDOM_COLOR_CODE = 2
RANDOM_COLOR_CODE_1 = 6
RANDOM_COLOR_CODE_2 = 4

class GameTest(unittest.TestCase):
    
    def setUp(self):
        Robot.initHardwareDevices = mock.Mock(return_value="")
        self.robot = Robot(Queue.Queue())
        self.game = Game(self.robot, Queue.Queue())
        
    def test_aGameWhenCreatedMustHaveZeroPuckInItsList(self):
        self.assertTrue(len(self.game.listOfPucks) == 0)
        
    def test_aGameWhenCreatedMustNotBeFinished(self):
        self.assertFalse(self.game.isFinished())
        
    def test_aGameWhenCreatedMustNotHaveAPuckBeingProcessed(self):
        self.assertTrue(self.game.getPuckNumberBeingProcessed() == 0)
        
    def test_aGameWhenCreatedMustNotHaveAResistanceValue(self):
        self.assertTrue(self.game.getResistanceValue() == -1)
        
    def test_aGameWhenCreatedMustNotHaveAPucksOrientation(self):
        self.assertTrue(self.game.getPucksOrientation() == "")
        
    def test_aGameWhenCreatedMustNotHaveAPositionToReadInitialisedForLetterBoard(self):
        self.assertTrue(self.game.getPositionToReadInLetterBoard() == -1)
        
    def test_aGameWhenCreatedMustNotHaveAPositionToReadInitialisedForOrientationBoard(self):
        self.assertTrue(self.game.getPositionToReadInOrientationBoard() == -1)
        
    def test_aGameWhenThreePucksPlacedShouldBeFinished(self):
        puck1 = Puck(RANDOM_COLOR_CODE)
        puck1.setHasBeenPlaced(True)
        puck2 = Puck(RANDOM_COLOR_CODE_1)
        puck2.setHasBeenPlaced(True)
        puck3 = Puck(RANDOM_COLOR_CODE_2)
        puck3.setHasBeenPlaced(True)
        self.game.listOfPucks.append(puck1)
        self.game.listOfPucks.append(puck2)
        self.game.listOfPucks.append(puck3)
        self.assertTrue(self.game.isFinished())
        
    def test_aGameWhenNotThreePucksPlacedShouldNotBeFinished(self):
        puck1 = Puck(RANDOM_COLOR_CODE)
        puck1.setHasBeenPlaced(True)
        puck2 = Puck(RANDOM_COLOR_CODE_1)
        puck2.setHasBeenPlaced(False)
        puck3 = Puck(RANDOM_COLOR_CODE_2)
        puck3.setHasBeenPlaced(True)
        self.game.listOfPucks.append(puck1)
        self.game.listOfPucks.append(puck2)
        self.game.listOfPucks.append(puck3)
        self.assertFalse(self.game.isFinished())
