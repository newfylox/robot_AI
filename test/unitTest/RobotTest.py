#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
import unittest
from main.model.Robot import Robot
import Queue

class GameTest(unittest.TestCase):
    
    def setUp(self):
        Robot.initHardwareDevices = mock.Mock(return_value="")
        self.robot = Robot(Queue.Queue())
        
    def test_aRobotWhenCreatedHasZeroForAngle(self):
        self.assertTrue(self.robot.getFilteredAngle()==0)
        
    def test_aRobotWhenCreatedHasZeroForPosition(self):
        self.assertTrue(self.robot.getPosition().toString() == "(0.0, 0.0)")
        
    def test_aRobotWhenCreatedHasZeroForNumberOfUpdate(self):
        self.assertTrue(self.robot.getNumberOfUpdate() == 0)
