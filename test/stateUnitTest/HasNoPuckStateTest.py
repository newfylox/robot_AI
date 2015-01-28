import Queue
import unittest
from main.model.Game import Game
from main.model.Robot import Robot
import mock
from numpy.random.mtrand import randint
from main.model.Puck import Puck
from main.states.HasNoPuckState import HasNoPuckState


RANDOM_COLOR_CODE = randint(0,9)

class HasNoPuckStateTest(unittest.TestCase):

    def setUp(self):
        Robot.initHardwareDevices = mock.Mock(return_value="")
        Robot.moveToPosition = mock.Mock(return_value="")
        Robot.setLedOn = mock.Mock(return_value="")
        self.robot = Robot(Queue.Queue())
        self.aGame = Game(self.robot, Queue.Queue())
        self.aGame.currentState = HasNoPuckState(self.aGame)
        self.aGame.listOfPucks = [Puck(RANDOM_COLOR_CODE), Puck(RANDOM_COLOR_CODE), Puck(RANDOM_COLOR_CODE)]

    def test_whenGameDoAnActionStateGameStateShouldChangeAtTheEndIfTheGameIsNotFinished(self):
        self.aGame.listOfPucks[0].setHasBeenPlaced(True)
        self.aGame.listOfPucks[1].setHasBeenPlaced(True)
        self.aGame.listOfPucks[2].setHasBeenPlaced(True)
        self.aGame.doAction()
        self.assertTrue(self.aGame.getCurrentStateName() == "HasNoPuckState")
        
    def test_whenGameDoAnActionStateGameStateShouldNotChangeAtTheEndIfTheGameIsFinished(self):
        self.aGame.listOfPucks[0].setHasBeenPlaced(True)
        self.aGame.listOfPucks[1].setHasBeenPlaced(True)
        self.aGame.listOfPucks[2].setHasBeenPlaced(False)
        self.aGame.doAction()
        self.assertTrue(self.aGame.getCurrentStateName() == "NearPucksState")
        
