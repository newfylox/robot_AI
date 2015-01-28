import Queue
import unittest
from main.model.Game import Game
from main.model.Robot import Robot
import mock
from main.states.NearResistanceState import NearResistanceState
from main.states.NearLetterBoardState import NearLetterBoardState
from numpy.random.mtrand import randint
from main.model.Puck import Puck

RANDOM_COLOR_CODE = randint(0,9)

class NearLetterBoardStateTest(unittest.TestCase):

    def setUp(self):
        Robot.initHardwareDevices = mock.Mock(return_value="")
        Robot.rotateToAngle = mock.Mock(return_value="")
        Robot.findLetterInLetterBoard = mock.Mock(return_value="D")
        Robot.setCamMiddle = mock.Mock(return_value="")
        Robot.setCamUp = mock.Mock(return_value="")
        NearResistanceState.fetchResistance = mock.Mock(return_value="")
        self.robot = Robot(Queue.Queue())
        self.aGame = Game(self.robot, Queue.Queue())
        self.aGame.currentState = NearLetterBoardState(self.aGame)
        self.aGame.listOfPucks = [Puck(RANDOM_COLOR_CODE), Puck(RANDOM_COLOR_CODE), Puck(RANDOM_COLOR_CODE)]
        self.aGame.setPositionToReadInLetterBoard(2)

    def test_whenGameDoAnActionStateGameStateShouldChangeAtTheEnd(self):
        self.aGame.doAction()
        self.assertTrue(self.aGame.getCurrentStateName() == "HasReadLetterBoardState")
        
    def test_whenGameDoAnActionFirstPuckCornerShouldBeInitialized(self):
        self.aGame.doAction()
        self.assertTrue(self.aGame.listOfPucks[0].getCornerToBePlaced() == "D")     
        