import sys
import Queue
import threading
from main.model.Position import Position
from main.network.RobotSocket import RobotSocket

class ThreadedClientRobot(object):

    def __init__(self, queue, game):
        self.robotQueue = queue
        self.game = game
        
    def run(self):
        self.robotSocket = RobotSocket()
        self.robotSocket.startConnection(sys.argv[1])
        
        #Start the connection thread
        self.connectionThread = threading.Thread(target=self.runConnectionThread)
        self.connectionThread.daemon = True
        self.connectionThread.start()
        
        while True:
            self.processDataInQueue()
             
    def runConnectionThread(self):    
        receivedCommand = ''
        while receivedCommand != 'quit':
            try : 
                receivedCommand = self.robotSocket.receiveDataFromBaseStation()
                print "The Robot has received the following command :  " + receivedCommand
                self.robotQueue.put(receivedCommand)
            except :
                pass

        self.robotSocket.stopConnection()
        self.game.isKilled = True
        if self.connectionThread.isAlive():
            try:
                    self.connectionThread._Thread__stop()
            except:
                    print(str(self.connectionThread.getName()) + 'could not be terminated')
        
    
    def processDataInQueue(self):
            while self.robotQueue.qsize():         
                try:
                    msg = self.robotQueue.get(0)
                    print "The robot has received the following in his robotQueue : " + str(msg)
                    if msg == "START":
                        self.game.start()       
                    elif msg == "STOP":
                        self.game.stop()
                    elif msg == "RESET":
                        self.game.reset()
                    elif msg == "TURNALITTLE":
                        self.game.robot.rotateCounterClockwise(30)
                    elif "OBSTACLESPOSITION" in msg:
                        splittedList = msg.split('-');
                        p1 = Position(splittedList[1],splittedList[2])
                        p2 = Position(splittedList[3],splittedList[4])
                        self.game.robot.obstacleOnePosition = p1
                        self.game.robot.obstacleTwoPosition = p2
                        self.game.robot.obstaclesPositionFetched = True
                    elif msg[:17] == "REFRESHEDPOSITION":
                            splittedList = msg.split('-', 3 );
                            if splittedList[1] == "None" or splittedList[2] == "None" or splittedList[3] == "None":
                                pass
                            else:                            
                                refreshedPosition = Position(splittedList[1], splittedList[2])
                                refreshedAngle = float(splittedList[3])
                                self.game.robot.setPosition(refreshedPosition)
                                self.game.robot.setAngle(refreshedAngle)
                            self.game.robot.numberOfUpdates = self.game.robot.numberOfUpdates + 1
                    elif msg[:14] == "REFRESHEDANGLE":
                            splittedList = msg.split('-', 1 );
                            if splittedList[1] == "None":
                                pass
                            else:                           
                                refreshedAngle = float(splittedList[1])
                                self.game.robot.setAngle(refreshedAngle)
                            self.game.robot.numberOfUpdates = self.game.robot.numberOfUpdates + 1
                    elif msg[:10] == "DIRECTIONS":
                        splittedDirectionList = msg.split('-')
                        splittedDirectionList.remove("DIRECTIONS")
                        if "" in splittedDirectionList:
                            splittedDirectionList.remove("")
                        self.game.robot.listOfDirections = splittedDirectionList
                        self.game.robot.numberOfUpdates = self.game.robot.numberOfUpdates + 1
                    else:
                        if msg != "":
                            self.robotSocket.sendDataToBaseStation(msg)                     
                except Queue.Empty:
                    pass
                
