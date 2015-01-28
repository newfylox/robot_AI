import Queue
import unittest
from main.model.Game import Game
from main.model.Robot import Robot
import mock
from numpy.random.mtrand import randint
from main.states.NearPucksState import NearPucksState
from main.model.Puck import Puck

RANDOM_COLOR_CODE = randint(0,9)

class NearPucksStateTest(unittest.TestCase):

    def setUp(self):
        Robot.initHardwareDevices = mock.Mock(return_value="")
        Robot.moveBackward = mock.Mock(return_value="")
        Robot.grabPuck = mock.Mock(return_value="")
        Robot.rotateToAngle = mock.Mock(return_value="")
        Robot.rotateClockwise = mock.Mock(return_value="")
        Robot.rotateCounterClockwise = mock.Mock(return_value="")
        Robot.moveBackward = mock.Mock(return_value="")
        Robot.moveForward = mock.Mock(return_value="")
        Robot.setCamMiddle = mock.Mock(return_value="")
        Robot.setCamDown = mock.Mock(return_value="")
        Robot.getDistanceToPuck = mock.Mock(return_value=(20,15))
        self.robot = Robot(Queue.Queue())
        self.aGame = Game(self.robot, Queue.Queue())
        self.aGame.puckNumberBeingProcessed = 0
        self.aGame.listOfPucks = [Puck(RANDOM_COLOR_CODE), Puck(RANDOM_COLOR_CODE), Puck(RANDOM_COLOR_CODE)]
        self.aGame.currentState = NearPucksState(self.aGame)

    def test_whenGameDoAnActionStateGameStateShouldChangeAtTheEnd(self):
        self.aGame.doAction()
        print self.aGame.getCurrentStateName()
        self.assertTrue(self.aGame.getCurrentStateName() == "HasPuckState")
