import Queue
import unittest
from main.model.Game import Game
from main.model.Robot import Robot
import mock
from numpy.random.mtrand import randint
from main.states.HasPuckState import HasPuckState

RANDOM_COLOR_CODE = randint(0,9)

class HasPuckStateTest(unittest.TestCase):

    def setUp(self):
        Robot.initHardwareDevices = mock.Mock(return_value="")
        Robot.moveToPosition = mock.Mock(return_value="")
        self.robot = Robot(Queue.Queue())
        self.aGame = Game(self.robot, Queue.Queue())
        self.aGame.currentState = HasPuckState(self.aGame)

    def test_whenGameDoAnActionStateGameStateShouldChangeAtTheEnd(self):
        self.aGame.doAction()
        self.assertTrue(self.aGame.getCurrentStateName() == "NearGoalPositionState")
        