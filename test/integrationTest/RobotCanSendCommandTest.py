import unittest
from main.network.BaseStationSocket import BaseStationSocket
from main.network.RobotSocket import RobotSocket

A_SERVER_IP_ADDRESS = 'localhost'
A_COMMAND = '[0,0,0]'

class RobotCanSendCommandTest(unittest.TestCase):

    def setUp(self):
        self.aRobotSocket = RobotSocket()
        self.aRobotSocket.startConnection(A_SERVER_IP_ADDRESS)
        self.aBaseStationSocket = BaseStationSocket()
        self.aBaseStationSocket.startConnection(A_SERVER_IP_ADDRESS)
        
    def tearDown(self):
        self.aRobotSocket.stopConnection()
        self.aBaseStationSocket.stopConnection()
        
    def test_whenRobotSendsACommandTheBaseStationReceivesTheCommand(self):
        self.aRobotSocket.sendDataToBaseStation(A_COMMAND)
        receivedCommand = self.aBaseStationSocket.receiveDataFromRobot()
        self.assertTrue(receivedCommand == A_COMMAND)
        
    def test_whenRobotSendsTwoCommandsTheBaseStationReceivesTowSameCommands(self):
        self.aRobotSocket.sendDataToBaseStation(A_COMMAND)
        firstReceivedCommand = self.aBaseStationSocket.receiveDataFromRobot()
        self.assertTrue(firstReceivedCommand == A_COMMAND)
        
    def test_whenRobotSendsACommandTheBaseStationSendsTheSameCommandToConfirm(self):
        self.aRobotSocket.sendDataToBaseStation(A_COMMAND)
        receivedCommand = self.aBaseStationSocket.receiveDataFromRobot()
        self.aBaseStationSocket.sendDataToRobot(receivedCommand)
        confirmedCommand = self.aRobotSocket.receiveDataFromBaseStation()
        self.assertEqual(A_COMMAND, confirmedCommand)