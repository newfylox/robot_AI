import unittest
from main.network.BaseStationSocket import BaseStationSocket
from main.network.RobotSocket import RobotSocket

A_SERVER_IP_ADDRESS = 'localhost'
A_COMMAND = '[0,0,0]'

class BaseStationCanSendCommandTest(unittest.TestCase):

    def setUp(self):
        self.aRobotSocket = RobotSocket()
        self.aRobotSocket.startConnection(A_SERVER_IP_ADDRESS)
        self.aBaseStationSocket = BaseStationSocket()
        self.aBaseStationSocket.startConnection(A_SERVER_IP_ADDRESS)
        
    def tearDown(self):
        self.aRobotSocket.stopConnection()
        self.aBaseStationSocket.stopConnection()
        
    def test_whenBaseStationSendsACommandTheRobotReceivesTheCommand(self):
        self.aBaseStationSocket.sendDataToRobot(A_COMMAND)
        receivedCommand = self.aRobotSocket.receiveDataFromBaseStation()
        self.assertTrue(receivedCommand == A_COMMAND)
        
    def test_whenBaseStationSendsTwoCommandsTheRobotReceivesTowSameCommands(self):
        self.aBaseStationSocket.sendDataToRobot(A_COMMAND)
        firstReceivedCommand = self.aRobotSocket.receiveDataFromBaseStation()
        self.aBaseStationSocket.sendDataToRobot(A_COMMAND)
        secondReceivedCommand = self.aRobotSocket.receiveDataFromBaseStation()
        self.assertTrue(firstReceivedCommand == A_COMMAND and secondReceivedCommand == A_COMMAND)
        
    def test_whenBaseStationSendsACommandTheRobotSendsTheSameCommandToConfirm(self):
        self.aBaseStationSocket.sendDataToRobot(A_COMMAND)
        receivedCommand = self.aRobotSocket.receiveDataFromBaseStation()
        self.aRobotSocket.sendDataToBaseStation(receivedCommand)
        confirmedCommand = self.aBaseStationSocket.receiveDataFromRobot()
        self.assertEqual(A_COMMAND, confirmedCommand)