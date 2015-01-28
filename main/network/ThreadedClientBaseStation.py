#!/usr/bin/env python
# -*- coding: utf-8 -*

import Queue
import sys
import threading
from main.GUI.EnterIPWindow import EnterIPWindow
from main.GUI.Gui import Gui
from main.network.BaseStationSocket import BaseStationSocket
from main.vision.Kinect import Kinect
from main.model.TrajectoryPlanner import TrajectoryPlanner
from main.model.Map import Map
from main.model.Position import Position
import time
import numpy


class ThreadedClientBaseStation:
    
    def __init__(self, master):
        self.robotQueue = Queue.Queue()
        self.kinect = Kinect()
        
        # Set up the GUI part
        self.gui = Gui(master, self.robotQueue)
        self.master = master
        self.obstaclesFound = False
        self.currentPath = []
        self.numberOfPath = 0
        
        # Start the connection
        self.baseStation = BaseStationSocket()
        self.baseStation.startConnection(EnterIPWindow().serverAddress)
         
        # Set up the thread for the connection with the robot
        self.connectionThread = threading.Thread(target=self.runConnectionThread)
        self.connectionThread.daemon = True
        self.connectionThread.start()
         
        # Set up the thread for the kinect to calculate the robot position in real time 
        self.kinectThread = threading.Thread(target=self.runKinectThread)
        self.kinectThread.daemon = True
        self.kinectThread.start()
        
        self.gameInProcess = False
        self.guiRunning = True
        self.obstacleOnePosition = Position(0, 0)
        self.obstacleTwoPosition = Position(0, 0)
        
        self.cornerAPlaced = False
        self.cornerBPlaced = False
        self.cornerCPlaced = False
        self.cornerDPlaced = False
        
        self.gui.ourBaseStationInterface.mainWindow.gameBoard.addPiece("robot", self.gui.ourBaseStationInterface.mainWindow.robotIcon, -11, -11)
        
        # Start the periodic call in the GUI to check if the robotQueue contains
        # anything        
        self.periodicCallToCheckGui()
 
    def sendDirections(self, receivedString): 
        splittedList = receivedString.split('-');  
        startPosition = Position(splittedList[1], splittedList[2])
        endPosition = Position(splittedList[3], splittedList[4])
        
        robotMap = Map(5)
        robotMap.addObstacle(self.obstacleOnePosition)
        robotMap.addObstacle(self.obstacleTwoPosition)
        
        if self.cornerAPlaced == "A":
            robotMap.addPuck("A")
        elif self.cornerBPlaced == "B":
            robotMap.addPuck("B")
        elif self.cornerCPlaced == "C":
            robotMap.addPuck("C")
        elif self.cornerDPlaced == "D":
            robotMap.addPuck("D")
        
        
        planner = TrajectoryPlanner(robotMap, False)
        returnedDirections, path = planner.getDirections(startPosition, endPosition) 
        self.currentPath = path
        self.gui.currentPathList = path
        self.numberOfPath = self.numberOfPath + 1
        self.robotQueue.put("UP")

        if returnedDirections == "STARTNOTFREE":
            self.baseStation.sendDataToRobot("DIRECTIONS-STARTNOTFREE")
        elif returnedDirections == "NOTHINGTODO":
            self.baseStation.sendDataToRobot("DIRECTIONS-NOTHING") 
        else: 
            stringToSend = "DIRECTIONS-" + str(returnedDirections) 
            self.baseStation.sendDataToRobot(stringToSend) 
        
    def sendObtaclesPositions(self):
        self.kinect.setToBusy()
        listPositions = self.kinect.getTower()

        numberOfTrys = 0
        while listPositions == None and numberOfTrys < 10:
            numberOfTrys = numberOfTrys + 1
            listPositions = self.kinect.getTower()
        if listPositions == None:
            time.sleep(20)
        else:
            message = "OBSTACLESPOSITION-" + str(listPositions[0]) + "-" + str(listPositions[1]) + "-" + str(listPositions[2]) + "-" + str(listPositions[3])
            p1 = Position(listPositions[0], listPositions[1])
            p2 = Position(listPositions[2], listPositions[3])
            self.obstacleOnePosition = p1
            self.obstacleTwoPosition = p2
            self.baseStation.sendDataToRobot(message)
            self.obstaclesFound = True
        self.kinect.setToNotBusy()
        
    def updateRobotPosition(self):
        if self.kinect.isBusy() == True:
            self.kinect.awaitingToWork = True
        while self.kinect.isBusy():
            time.sleep(0.5)
        self.kinect.setToBusy()
        
        listOfPositionsX = []
        listOfPositionsY = []
    
        self.kinect.getPosition()
        numberOfIterations = 0
        while len(listOfPositionsX) < 3 and numberOfIterations < 10:
            positionX, positionY = self.kinect.getPosition()
            if positionX[0] != None:
                listOfPositionsX.append(positionX[0])
            if positionY[0] != None:
                listOfPositionsY.append(positionY[0])
            numberOfIterations = numberOfIterations + 1
        
        if positionX[0] == None or positionY[0] == None:
            self.baseStation.sendDataToRobot("TURNALITTLE")
            time.sleep(5)
            numberOfIterations = 0
            while len(listOfPositionsX) < 3 and numberOfIterations < 10:
                positionX, positionY = self.kinect.getPosition()
                if positionX[0] != None:
                    listOfPositionsX.append(positionX[0])
                if positionY[0] != None:
                    listOfPositionsY.append(positionY[0])
                numberOfIterations = numberOfIterations + 1  
                if positionX[0] == None or positionY[0] == None:
                    print "Failed to fetch position"
                else:
                    finalPositionX = self.median(listOfPositionsX)
                    finalPositionY = self.median(listOfPositionsY)
        else:    
            finalPositionX = numpy.median(listOfPositionsX)
            finalPositionY = numpy.median(listOfPositionsY)

        listAngles = []

        self.kinect.getAngle()
        numberOfIterations = 0
        while len(listAngles) < 4 and numberOfIterations < 10:
            angle = self.kinect.getAngle()
            if angle != None:
                listAngles.append(angle)
            numberOfIterations = numberOfIterations + 1        

        self.hasTurned = False

        msg = "REFRESHEDPOSITION-" + str(finalPositionX) + "-" + str(finalPositionY) + "-" + str(angle)
        self.baseStation.sendDataToRobot(msg)
        self.kinect.setToNotBusy()
        
    def updateRobotAngle(self):  
        if self.kinect.isBusy() == True:
            self.kinect.awaitingToWork = True
            
        while self.kinect.isBusy():
            time.sleep(0.5)
        self.kinect.setToBusy()

        listAngles = []

        self.kinect.getAngle()
        numberOfIterations = 0
        while len(listAngles) < 4 and numberOfIterations < 10:
            angle = self.kinect.getAngle()
            if angle != None:
                listAngles.append(angle)
            numberOfIterations = numberOfIterations + 1
        if angle == None:
            self.baseStation.sendDataToRobot("REFRESHEDANGLE-" + str("None"))
            self.kinect.setToNotBusy()
            self.kinect.awaitingToWork = False
                
        else:
            finalAngle = numpy.median(listAngles)
            self.baseStation.sendDataToRobot("REFRESHEDANGLE-" + str(finalAngle))
            self.kinect.setToNotBusy()
            self.kinect.awaitingToWork = False
        
    def periodicCallToCheckGui(self):
        # The GUI will check if it has to update something
        self.gui.processDataInQueue()
        
        if self.gui.ourBaseStationInterface.mainWindow.windowHasBeenClosed == True:
            self.guiRunning = False

        if self.gui.ourBaseStationInterface.mainWindow.buttonResetHasBeenPushed == True:
            self.baseStation.sendDataToRobot("RESET")
            self.gui.ourBaseStationInterface.mainWindow.buttonResetHasBeenPushed = False
            self.gui.ourBaseStationInterface.mainWindow.status = "Stopped"
            self.gui.ourBaseStationInterface.status = "Stopped"
            self.gui.robotQueue.put("RESET")
            self.hasTurned = False
            self.cornerAPlaced = False
            self.cornerBPlaced = False
            self.cornerCPlaced = False
            self.cornerDPlaced = False
            self.obstaclesPositionsFetched = False
            self.obstaclesFound = False
        
        if self.gui.ourBaseStationInterface.mainWindow.state == True:
            if self.gameInProcess == False:
                self.baseStation.sendDataToRobot("START")
                self.gameInProcess = True

        if self.gui.ourBaseStationInterface.mainWindow.state == False:
            if self.gameInProcess == True:
                self.baseStation.sendDataToRobot("STOP")
                self.gameInProcess = False
                  
        if self.guiRunning == False:
            # sending the robot to quit so it closes 
            self.baseStation.sendDataToRobot("quit")
            self.gui.ourBaseStationInterface.root.destroy()
            if self.connectionThread.isAlive():
                try:
                    self.connectionThread._Thread__stop()
                except:
                    print(str(self.connectionThread.getName()) + ' could not be terminated')
            if self.kinectThread.isAlive():
                try:
                    self.kinectThread._Thread__stop()
                except:
                    print(str(self.kinectThread.getName()) + ' could not be terminated')
            
            sys.exit(1)
        
        self.master.after(100, self.periodicCallToCheckGui)
        
    def runConnectionThread(self):    
        receivedCommand = ''
        while receivedCommand != 'quit':
            print "runConnectionThread"
            try : 
                receivedCommand = self.baseStation.receiveDataFromRobot()
                print "The base station has received the following command : " + str(receivedCommand)
                if receivedCommand == "REQUESTPOSITION":
                    # Ancienne option:
                    self.updateRobotPosition()
                elif receivedCommand == "REQUESTANGLE":
                    # Ancienne option:
                    self.updateRobotAngle()
                elif receivedCommand == "REQUESTOBSTACLES":
                    self.sendObtaclesPositions()
                elif receivedCommand == "GAMEFINISHED":
                    self.gui.ourBaseStationInterface.mainWindow.finished = True
                elif receivedCommand == "STARTRECEIVED":
                    self.gui.ourBaseStationInterface.status = "The robot started."
                elif "GETDIRECTIONS" in receivedCommand:
                    self.sendDirections(receivedCommand)
                elif "ADDPUCK" in receivedCommand:
                    splittedList = receivedCommand.split('-');  
                    corner = splittedList[1]
                    color = splittedList[2]
                    if corner == "A":
                        string = "PP-" + "A" + "-" + str(color)
                        self.robotQueue.put(string)
                        self.cornerAPlaced = True
                    elif corner == "B":
                        string = "PP-" + "B" + "-" + str(color)
                        self.robotQueue.put(string)
                        self.cornerBPlaced = True
                    elif corner == "C":
                        string = "PP-" + "C" + "-" + str(color)
                        self.robotQueue.put(string)
                        self.cornerCPlaced = True
                    elif corner == "D":
                        string = "PP-" + "D" + "-" + str(color)
                        self.robotQueue.put(string)
                        self.cornerDPlaced = True
                else:
                    self.robotQueue.put(receivedCommand)
            except :
                pass

        self.baseStation.stopConnection()
        
    def runKinectThread(self):  
        mapUtil = Map(5)
        self.ObstaclesPutOnMap = False
        
        while True:
            self.hasTurned = False
            if self.kinect.isBusy() == False and self.kinect.awaitingToWork == False:
                self.kinect.setToBusy()
                pX, pY = self.kinect.getPosition()
                if pX == None or pY == None:
                    pass
                else:
                    robotI, robotJ = mapUtil.translatePositionXYToPositionIJ(Position(pX, pY))
                    string = "R-" + str(robotI) + "-" + str(robotJ)
                    self.robotQueue.put(string)
                self.kinect.setToNotBusy()
            if self.obstaclesFound == True and self.ObstaclesPutOnMap == False:
                obstacleI_1, obstacleJ_1 = mapUtil.translatePositionXYToPositionIJ(self.obstacleOnePosition)
                obstacleI_2, obstacleJ_2 = mapUtil.translatePositionXYToPositionIJ(self.obstacleTwoPosition)
                string = "O-" + str(obstacleI_1) + "-" + str(obstacleJ_1) + "-" + str(obstacleI_2) + "-" + str(obstacleJ_2)
                self.robotQueue.put(string)
                self.ObstaclesPutOnMap = True
                time.sleep(1)
            time.sleep(5)
         

            