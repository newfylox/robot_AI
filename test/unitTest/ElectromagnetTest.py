import unittest
from main.model.Electromagnet import Electromagnet
from mock import MagicMock
from main.GUI.hardware.MicroDue import MicroDue
from main.GUI.hardware.Pololu import Pololu

class ElectromagnetTest(unittest.TestCase):
 
    def setUp(self):
        self.mockMicroDue = MagicMock(MicroDue)
        self.mockPololu = MagicMock(Pololu)
        self.anElectromagnet = Electromagnet(self.mockMicroDue, self.mockPololu)

    def test_whenAnElectromagnetIsCreatedItMustBeDesactivated(self):
        self.assertFalse(self.anElectromagnet.isActivated())
        
    def test_AnElectromagnetWhenActivatedMustBecomeActivated(self):
        self.anElectromagnet.activate()
        self.assertTrue(self.anElectromagnet.isActivated())
        
    def test_AnElectromagnetWhenActivatedWhenActiveMustKeepBeingActivated(self):
        self.anElectromagnet.activate()
        self.anElectromagnet.activate()
        self.assertTrue(self.anElectromagnet.isActivated())
        
    def test_AnElectromagnetWhenDesactivatedMustBecomeDesactivated(self):
        self.anElectromagnet.activate()
        self.anElectromagnet.desactivate()
        self.assertFalse(self.anElectromagnet.isActivated())
        
    def test_AnElectromagnetWhenDesactivatedWhenNotActiveMustKeepBeingDesactivated(self):
        self.anElectromagnet.desactivate()
        self.anElectromagnet.desactivate()
        self.assertFalse(self.anElectromagnet.isActivated())


