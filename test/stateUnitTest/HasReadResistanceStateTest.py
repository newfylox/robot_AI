import Queue
import unittest
from main.model.Game import Game
from main.model.Robot import Robot
import mock
from main.states.HasReadResistanceState import HasReadResistanceState

RED_COLOR_CODE = 2
GREEN_COLOR_CODE = 5
ORANGE_COLOR_CODE = 3

class HasReadResistanceStateTest(unittest.TestCase):

    def setUp(self):
        Robot.initHardwareDevices = mock.Mock(return_value="")
        Robot.moveToPosition = mock.Mock(return_value="")
        Robot.rotateToAngle = mock.Mock(return_value="")
        self.robot = Robot(Queue.Queue())
        self.aGame = Game(self.robot, Queue.Queue())
        self.aGame.currentState = HasReadResistanceState(self.aGame)
        self.aGame.setResistanceValue(25000)
        HasReadResistanceState.splitResistanceValueInThreeNumbers = mock.Mock(return_value=(2,5,3))
        
    def test_whenGameDoAnActionStateGameStateShouldChangeAtTheEnd(self):
        self.aGame.doAction()
        self.assertTrue(self.aGame.getCurrentStateName() == "NearLetterBoardState")
        
    def test_whenGameDoAnActionPositionToReadInLetterBoardShouldChange(self):
        self.aGame.doAction()
        self.assertFalse(self.aGame.getPositionToReadInLetterBoard() == -1)     
        
    def test_whenGameDoAnActionPositionToReadInOrientationBoardShouldChange(self):
        self.aGame.doAction()
        self.assertFalse(self.aGame.getPositionToReadInOrientationBoard() == -1) 
        
    def test_whenGameDoAnActionListOfPucksShouldHaveThreePucks(self):
        self.aGame.doAction()
        self.assertTrue(len(self.aGame.listOfPucks) == 3)   
        
    def test_whenGameDoAnActionPuckInListShouldNotBePlaced(self):
        self.aGame.doAction()
        self.assertFalse(self.aGame.listOfPucks[0].hasBeenPlaced) 
        
    def test_whenGameDoAnActionPucksInListShouldNotHavePriorityToMinusOne(self):
        self.aGame.doAction()
        aPuckWithPriorityToMinusOneExist = False
        for puck in self.aGame.listOfPucks:
            if puck.getPriority() == -1:
                aPuckWithPriorityToMinusOneExist = True
        self.assertFalse(aPuckWithPriorityToMinusOneExist)
        
    def test_whenGameDoAnActionPuckInListShouldHaveCornerToBePlacedToNothing(self):
        self.aGame.doAction()
        self.assertTrue(self.aGame.listOfPucks[0].getCornerToBePlaced() == "")
        
    def test_whenGameDoAnActionWithResistanceValue25000PucksColorShouldBeRedGreenOrange(self):
        self.aGame.doAction()
        gameHasARedPuck = False
        gameHasAGreenPuck = False        
        gameHasAOrangePuck = False 
        for puck in self.aGame.listOfPucks:
            if puck.getPrimaryColor() == RED_COLOR_CODE:
                gameHasARedPuck = True
            if puck.getPrimaryColor() == ORANGE_COLOR_CODE:
                gameHasAGreenPuck = True                
            if puck.getPrimaryColor() == GREEN_COLOR_CODE:
                gameHasAOrangePuck = True
        self.assertTrue(gameHasARedPuck)
        self.assertTrue(gameHasAGreenPuck)
        self.assertTrue(gameHasAOrangePuck)
        
    def test_whenGameDoAnActionWithResistanceValue25000PositionToReadInLetterBoardShouldBeTwo(self):
        self.aGame.doAction()
        self.assertTrue(self.aGame.getPositionToReadInLetterBoard() == 2)
        
    def test_whenGameDoAnActionWithResistanceValue25000PositionToReadInOrientationBoardShouldBeFive(self):
        self.aGame.doAction()
        self.assertTrue(self.aGame.getPositionToReadInOrientationBoard() == 3)

        

        

        

    
