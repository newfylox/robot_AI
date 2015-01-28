import unittest

from main.model.Map import Map
from main.model.Position import Position

A_CELL_DIMENSION = 2

class PuckTest(unittest.TestCase):

    def setUp(self):
        self.aMap = Map(A_CELL_DIMENSION)
        
    def test_whenAMapIsCreatedCellDimensionMustBeTheRight(self):
        self.assertTrue(self.aMap.getCellDimension() == A_CELL_DIMENSION)
        
    def test_ifObstacleAtAPositionCellShouldNotBeFree(self):
        self.aMap.addObstacle(Position(3,3))
        self.assertFalse(self.aMap.isPositionXYFree(Position(3,3)))
        
    def test_ifPuckAtAPositionCellShouldNotBeFree(self):
        self.aMap.addPuck(Position(15,15))
        self.assertFalse(self.aMap.isPositionXYFree(Position(15,15)))
        
    def test_ifWallExpandPositionNearWallShouldNotBeFree(self):
        self.aMap.expandWalls()
        self.assertFalse(self.aMap.isPositionXYFree(Position(0,0)))
        
    def test_ifWallExpandPositionNotNearWallShouldBeFree(self):
        self.aMap.expandWalls()
        self.assertTrue(self.aMap.isPositionXYFree(Position(20,20)))

        




        

    
