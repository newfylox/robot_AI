import Queue
import unittest
from main.model.Game import Game
from main.model.Robot import Robot
import mock

class NoResistanceValueStateTest(unittest.TestCase):

    def setUp(self):
        Robot.initHardwareDevices = mock.Mock(return_value="")
        Robot.moveRight = mock.Mock(return_value="")
        Robot.moveBackward = mock.Mock(return_value="")
        Robot.refreshPositionAndAngle = mock.Mock(return_value="")
        Robot.rotateToAngle = mock.Mock(return_value="")
        self.robot = Robot(Queue.Queue())
        self.aGame = Game(self.robot, Queue.Queue())

    def test_whenGameDoAnActionInNoResistanceValueStateGameStateShouldChangeStateAtTheEnd(self):
        self.aGame.doAction()
        self.assertTrue(self.aGame.getCurrentStateName() == "NearResistanceState")
        

        

        

    
