import Queue
from main.GUI.BaseStationInterface import BaseStationInterface

class Gui:
    def __init__(self, master, queue):
        self.robotQueue = queue
        self.ourBaseStationInterface = BaseStationInterface(master) 
        self.currentPathList=[]

    def processDataInQueue(self):
        #Handle all the messages currently in the robotQueue (if any).
        while self.robotQueue.qsize():
            try:
                msg = self.robotQueue.get(0)
                # Check contents of message and do what it says
                #Update the path
                if(msg == "UP"):
                    self.ourBaseStationInterface.mainWindow.gameBoard.addPath(self.currentPathList, self.ourBaseStationInterface.mainWindow.pathIcon)
                #Update obstacles
                if(msg[:2] == "O-"):
                    splittedList = msg.split('-');
                    obstacleCoords1 = (int(splittedList[1]), int(splittedList[2]))
                    obstacleCoords2 = (int(splittedList[3]), int(splittedList[4]))
                    self.ourBaseStationInterface.mainWindow.gameBoard.addObstacle("obstacle1", obstacleCoords1)
                    self.ourBaseStationInterface.mainWindow.gameBoard.addObstacle("obstacle2", obstacleCoords2)
                #Update the robot
                if(msg[:2] == "R-"):
                    splittedList = msg.split('-');
                    ri = int(splittedList[1])
                    rj = int(splittedList[2])
                    self.ourBaseStationInterface.mainWindow.gameBoard.placePiece("robot",ri,rj)
                #Change the color #1
                if(msg[:2] == "C1"):
                    self.ourBaseStationInterface.textColorOne = msg[3:]
                #Change the color #2   
                if(msg[:2] == "C2"):
                    self.ourBaseStationInterface.textColorTwo = msg[3:]
                #Change the color #3  
                if(msg[:2] == "C3"):
                    self.ourBaseStationInterface.textColorThree = msg[3:]
                #Change the resistance value  
                if(msg[:2] == "RV"):
                    self.ourBaseStationInterface.resistanceValueLabel = msg[3:]
                #Set the pucks placed 
                if(msg[:2] == "PP"):
                    splittedList = msg.split('-');
                    corner = splittedList[1]
                    color = splittedList[2]
                    if corner == "A":
                        pos = (17,17)
                    elif corner == "B":
                        pos = (17,4)
                    elif corner == "C":
                        pos = (4,4)
                    elif corner == "D":
                        pos = (4,17)
                    stringPColor = "p-" + color
                    self.ourBaseStationInterface.mainWindow.gameBoard.addPuck(stringPColor, pos)
                #Put a puck in corner A   
                if(msg[:2] == "A-"):
                    self.ourBaseStationInterface.textCornerAColor = msg[2:]
                    self.ourBaseStationInterface.puckCornerAVisible = True
                #Put a puck in corner B    
                if(msg[:2] == "B-"):
                    self.ourBaseStationInterface.textCornerBColor = msg[2:]
                    self.ourBaseStationInterface.puckCornerBVisible = True
                #Put a puck in corner C    
                if(msg[:2] == "C-"):
                    self.ourBaseStationInterface.textCornerCColor = msg[2:]
                    self.ourBaseStationInterface.puckCornerCVisible = True
                #Put a puck in corner D    
                if(msg[:2] == "D-"):
                    self.ourBaseStationInterface.textCornerDColor = msg[2:]
                    self.ourBaseStationInterface.puckCornerDVisible = True      
                #Put the letter in the board     
                if(msg[:3] == "LP-"):
                    self.ourBaseStationInterface.textLetterBoard = msg[3]
                    self.ourBaseStationInterface.positionXLetterBoard = msg[5:8] 
                    self.ourBaseStationInterface.positionYLetterBoard = msg[9:]   
                #Put the orientation in the board    
                if(msg[:3] == "OP-"):
                    self.ourBaseStationInterface.textOrientationBoard = msg[3:5]
                    self.ourBaseStationInterface.positionXOrientationBoard = msg[6:9] 
                    self.ourBaseStationInterface.positionYOrientationBoard = msg[10:]  
                #Reset the gui at its original set
                if(msg[:5] == "RESET"):
                    self.ourBaseStationInterface.positionXLetterBoard = 999 
                    self.ourBaseStationInterface.positionYLetterBoard = 999 
                    self.ourBaseStationInterface.positionXOrientationBoard = 999
                    self.ourBaseStationInterface.positionYOrientationBoard = 999 
                    self.ourBaseStationInterface.textLetterBoard = ""
                    self.ourBaseStationInterface.textOrientationBoard = ""
                    self.ourBaseStationInterface.puckCornerAVisible = False  
                    self.ourBaseStationInterface.puckCornerBVisible = False  
                    self.ourBaseStationInterface.puckCornerCVisible = False  
                    self.ourBaseStationInterface.puckCornerDVisible = False  
                    self.ourBaseStationInterface.resistanceValueLabel = 0
                    self.ourBaseStationInterface.textColorOne = "GREY"
                    self.ourBaseStationInterface.textColorTwo = "GREY"
                    self.ourBaseStationInterface.textColorThree = "GREY"
            except Queue.Empty:
                pass
            