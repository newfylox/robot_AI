import Queue
import unittest
from main.model.Game import Game
from main.model.Robot import Robot
import mock
from main.states.NearResistanceState import NearResistanceState

class NearResistanceStateTest(unittest.TestCase):

    def setUp(self):
        Robot.initHardwareDevices = mock.Mock(return_value="")
        Robot.moveLeft = mock.Mock(return_value="")
        Robot.moveRight = mock.Mock(return_value="")
        Robot.moveBackward = mock.Mock(return_value="")
        Robot.moveForward = mock.Mock(return_value="")
        Robot.refreshPositionAndAngle = mock.Mock(return_value="")
        Robot.rotateToAngle = mock.Mock(return_value="")
        NearResistanceState.requestObstaclesPositions = mock.Mock(return_value="")
        Robot.readResistance = mock.Mock(return_value=2000)
        self.robot = Robot(Queue.Queue())
        self.aGame = Game(self.robot, Queue.Queue())
        self.aGame.currentState = NearResistanceState(self.aGame)

    def test_whenGameDoAnActionInNearResistanceStateGameStateShouldChangeAtTheEnd(self):
        self.aGame.doAction()
        self.assertFalse(self.aGame.getCurrentStateName() == "HasReadResistanceState")
        
    def test_whenGameDoAnActionInNearResistanceStateResistanceValueShouldChange(self):
        self.aGame.doAction()
        self.assertFalse(self.aGame.getResistanceValue == -1)       
        

        

        

    
