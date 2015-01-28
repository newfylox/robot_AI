import unittest

from main.model.Puck import Puck

A_COLOR = 2

class PuckTest(unittest.TestCase):

    def setUp(self):
        self.aPuck = Puck(A_COLOR)
        
    def test_whenAPuckIsCreatedPriorityShouldBeMinusOne(self):
        self.assertTrue(self.aPuck.getPriority() == -1)



        

    
