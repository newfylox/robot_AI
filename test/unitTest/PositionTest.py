import unittest
from main.model.Position import Position

A_POSITION_X = 0
A_POSITION_Y = 0
A_NEW_POSITION_X = 1
A_NEW_POSITION_Y = 1

class PositionTest(unittest.TestCase):

    def setUp(self):
        self.aPosition = Position(A_POSITION_X, A_POSITION_Y)

    def test_getPositionXShouldReturnGoodX(self):
        self.assertTrue(self.aPosition.getX() == A_POSITION_X)
                        
    def test_getPositionXShouldReturnGoodY(self):
        self.assertTrue(self.aPosition.getX() == A_POSITION_Y)

    
