import Queue
import unittest
from main.model.Game import Game
from main.model.Robot import Robot
import mock
from numpy.random.mtrand import randint
from main.model.Puck import Puck
from main.states.NearPucksState import NearPucksState
from main.states.NearGoalPositionState import NearGoalPositionState


RANDOM_COLOR_CODE = randint(0,9)

class NearGoalPositionStateTest(unittest.TestCase):

    def setUp(self):
        Robot.initHardwareDevices = mock.Mock(return_value="")
        Robot.moveToPosition = mock.Mock(return_value="")
        Robot.moveToRight = mock.Mock(return_value="")
        Robot.moveForward = mock.Mock(return_value="")
        Robot.rotateToAngle = mock.Mock(return_value="")
        NearGoalPositionState.goToCorner = mock.Mock(return_value="")
        Robot.findLetterInLetterBoard = mock.Mock(return_value="D")
        Robot.dropPuck = mock.Mock(return_value="SA")
        NearPucksState.fetchPuck = mock.Mock(return_value="")
        self.robot = Robot(Queue.Queue())
        self.aGame = Game(self.robot, Queue.Queue())
        self.aGame.currentState = NearGoalPositionState(self.aGame)
        self.aGame.listOfPucks = [Puck(RANDOM_COLOR_CODE), Puck(RANDOM_COLOR_CODE), Puck(RANDOM_COLOR_CODE)]
        self.aGame.setPucksOrientation("SA")
        self.aGame.setPositionToReadInLetterBoard(2)
        self.aGame.listOfPucks[0].setCornerToBePlaced("D")

    def test_whenGameDoAnActionStateGameStateShouldChangeAtTheEnd(self):
        self.aGame.doAction()
        self.assertTrue(self.aGame.getCurrentStateName() == "HasNoPuckState")
        
    def test_whenGameDoAnActionAtTheEndOneMorePuckShouldBePlaced(self):
        numberOfPucksPlacedAtStart = self.aGame.getNumberOfPucksPlaced()
        self.aGame.doAction()
        numberOfPucksPlacedAfter = self.aGame.getNumberOfPucksPlaced()
        self.assertTrue(numberOfPucksPlacedAfter > numberOfPucksPlacedAtStart)
        
