import Queue
import unittest
from main.model.Game import Game
from main.model.Robot import Robot
import mock
from numpy.random.mtrand import randint
from main.model.Puck import Puck
from main.states.HasReadOrientationBoardState import HasReadOrientationBoardState

RANDOM_COLOR_CODE = randint(0,9)

class HasReadOrientationBoardStateTest(unittest.TestCase):

    def setUp(self):
        Robot.initHardwareDevices = mock.Mock(return_value="")
        Robot.moveLeft = mock.Mock(return_value="")
        Robot.moveRight = mock.Mock(return_value="")
        Robot.rotateToAngle = mock.Mock(return_value="")
        self.robot = Robot(Queue.Queue())
        self.aGame = Game(self.robot, Queue.Queue())
        self.aGame.currentState = HasReadOrientationBoardState(self.aGame)
        puck1 = Puck(RANDOM_COLOR_CODE)
        puck1.setPriority(1)
        puck2 = Puck(RANDOM_COLOR_CODE)
        puck2.setPriority(2)
        puck3 = Puck(RANDOM_COLOR_CODE)
        puck3.setPriority(1)
        self.aGame.listOfPucks = [puck1, puck2, puck3]
        self.aGame.setPucksOrientation("SA")
        self.aGame.listOfPucks[0].setCornerToBePlaced("D")
        self.aGame.setPositionToReadInOrientationBoard(3)

    def test_whenGameDoAnActionStateGameStateShouldChangeAtTheEnd(self):
        self.aGame.doAction()
        self.assertTrue(self.aGame.getCurrentStateName() == "NearPucksState")
        
    def test_puckListShouldBeResetAccordingToPriority(self):
        self.aGame.doAction()
        self.assertTrue(self.aGame.listOfPucks[0].getPriority() == 1)
        
    def test_whenGameDoAnActionPuckOneCornerShouldBeDWithSAOrientationAndDFirstCorner(self):
        self.aGame.doAction()
        self.assertTrue(self.aGame.listOfPucks[0].getCornerToBePlaced() == "D")
        
    def test_whenGameDoAnActionPuckTwoCornerShouldBeDWithSAOrientationAndDFirstCornerWithPrioritySetted(self):
        self.aGame.doAction()
        self.assertTrue(self.aGame.listOfPucks[1].getCornerToBePlaced() == "B")
        
    def test_whenGameDoAnActionPuckThreeCornerShouldBeDWithSAOrientationAndDFirstCornerWithPrioritySetted(self):
        self.aGame.doAction()
        self.assertTrue(self.aGame.listOfPucks[2].getCornerToBePlaced() == "C")

        
    def test_whenGameDoAnActionNoPuckShouldHavePriorityToMinusOne(self):
        self.aGame.doAction()
        allPuckHaveAPriority = True
        for puck in self.aGame.listOfPucks:
            if puck.getPriority() == -1:
                allPuckHaveAPriority = False
        self.assertTrue(allPuckHaveAPriority)
        
    def test_whenGameDoAnActionNoPuckShouldHaveCornerToNothing(self):
        self.aGame.doAction()
        allPuckHaveACorner = True
        for puck in self.aGame.listOfPucks:
            if puck.getCornerToBePlaced == "":
                allPuckHaveACorner = False
        self.assertTrue(allPuckHaveACorner)
        
    
