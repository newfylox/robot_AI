import Queue
import unittest
from main.model.Game import Game
from main.model.Robot import Robot
import mock
from main.states.NearResistanceState import NearResistanceState
from main.states.NearOrientationBoardState import NearOrientationBoardState
from numpy.random.mtrand import randint

RANDOM_COLOR_CODE = randint(0,9)
RED_COLOR_CODE = 2
ORANGE_COLOR_CODE = 3
GREEN_COLOR_CODE = 5

class NearOrientationBoardStateTest(unittest.TestCase):

    def setUp(self):
        Robot.initHardwareDevices = mock.Mock(return_value="")
        Robot.findOrientationInOrientationBoard = mock.Mock(return_value="SA")
        NearResistanceState.fetchResistance = mock.Mock(return_value="")
        self.robot = Robot(Queue.Queue())
        self.aGame = Game(self.robot, Queue.Queue())
        self.aGame.currentState = NearOrientationBoardState(self.aGame)
        self.aGame.setPositionToReadInOrientationBoard(2)


    def test_whenGameDoAnActionStatePuckOrientationShouldChange(self):
        self.aGame.doAction()
        self.assertTrue(self.aGame.getPucksOrientation() == "SA")
        
    def test_whenGameDoAnActionStateGameStateShouldChangeAtTheEnd(self):
        self.aGame.doAction()
        self.assertTrue(self.aGame.getCurrentStateName() == "HasReadOrientationBoardState")
  
