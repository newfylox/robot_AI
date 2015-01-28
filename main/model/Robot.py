#!/usr/bin/env python
# -*- coding: utf-8 -*- 
 
from main.model.Electromagnet import Electromagnet  
from main.model.Map import Map
from main.model.Position import Position
from main.model.TrajectoryPlanner import TrajectoryPlanner
from main.vision.Camera import Camera  
from math import sqrt
from main.constants import ANGLE_FOR_CARDINAL
from main.GUI.hardware.MicroDue import MicroDue
from main.GUI.hardware.Pololu import Pololu
import time


class Robot(object):

    def __init__(self, queue):
        self.robotQueue = queue

        self.position = Position(0, 0)
        self.angle = 0
        
        self.numberOfUpdates = 0

        self.map = Map(5)
        self.trajectoryPlanner = TrajectoryPlanner(self.map, False)
        self.obstaclesPositionFetched = False
        self.obstacleOnePosition = Position(0, 0)
        self.obstacleTwoPosition = Position(0, 0)
        self.listOfDirections = ""
        
        self.initHardwareDevices()
    
    def initHardwareDevices(self):
        self.microDue = MicroDue()
        self.pololu = Pololu()
        self.camera = Camera()
        self.electromagnet = Electromagnet(self.microDue, self.pololu)
        self.electromagnet.desactivate()
        self.electromagnet.goUp()
        
    def findLetterInLetterBoard(self, position):
        return self.camera.findLetterInLetterBoard(position)
        
    def findOrientationInOrientationBoard(self, position):
        return self.camera.findOrientationInOrientationBoard(position)
        
    def findColor(self, colorCode):
        return self.camera.findColor(colorCode)
    
    def getDistanceToCorner(self):
        return self.camera.getDistanceToCorner()
    
    def getDistanceToPuck(self, puckColorCode):
        return self.camera.getDistanceToPuck(puckColorCode)     
        
    def getPosition(self):
        return self.position
    
    def setPosition(self, newPosition):
        self.position = newPosition
        
    def getFilteredAngle(self):
        return self.angle
    
    def setAngle(self, newAngle):
        self.angle = newAngle

    def getNumberOfUpdate(self):
        return self.angle
    
    def incrementNumberOfUpdates(self, new):
        self.numberOfUpdates = self.numberOfUpdates + 1
        
    def refreshPositionAndAngle(self):
        self.robotQueue.put("REQUESTPOSITION")
        self.waitForUpdateToFinish()
            
    def refreshAngle(self):
        self.robotQueue.put("REQUESTANGLE")
        self.waitForUpdateToFinish()
        
    def moveToPosition(self, position):
        
        self.hasToDoSomething = True
        
        # Update its position
        self.refreshPositionAndAngle()  
        startPosition = self.position
        
        # Sending the request to get the list of directions
        directionString = "GETDIRECTIONS-" + str(startPosition.getX()) + "-" + str(startPosition.getY()) + "-" + str(position.getX()) + "-" + str(position.getY()) 
        self.robotQueue.put(directionString)
        self.waitForUpdateToFinish()
        listOfDirections = self.listOfDirections

        # If the trajectory planner tells us that we have no directions, already at the good place
        if listOfDirections[0] == "NOTHING":
            self.hasToDoSomething = False

        # If the trajectory planner tells us that we are trying to start at a invalid start position   
        if listOfDirections[0] == "STARTNOTFREE":
            self.rotateToAngle(0)
            self.moveBackward(20)
            self.refreshPositionAndAngle()  
            startPosition = self.position
            # Sending the request to get again the list of directions
            directionString = "GETDIRECTIONS-" + str(startPosition.getX()) + "-" + str(startPosition.getY()) + "-" + str(position.getX()) + "-" + str(position.getY()) 
            self.robotQueue.put(directionString)
            self.waitForUpdateToFinish()
            listOfDirections = self.listOfDirections
            
        #If there is directions to follow    
        if self.hasToDoSomething == True:
            for moves in listOfDirections:
                move = moves.split('*', 1)
                distance = 0
                if (len(move[1]) == 2):
                    distance = int(round(sqrt(2 * ((int(move[0]) * self.map.cellDimension) ** 2)), 0))  
                else:
                    distance = int(int(move[0]) * self.map.cellDimension)       
                self.rotateToAngle(ANGLE_FOR_CARDINAL.get(move[1]))
                self.moveForward(distance)      

    def moveLeft(self, distance):
        self.microDue.moveLeft(distance)
        
    def moveRight(self, distance):
        self.microDue.moveRight(distance)
        
    def moveForward(self, distance):
        self.microDue.moveForward(distance)
        
    def moveBackward(self, distance):
        self.microDue.moveBackward(distance)
        
    def setLedOn(self):
        self.microDue.setLedOn()
        
    def setLedOff(self):
        self.microDue.setElectroOff()
        
    def setCamMiddle(self):
        self.pololu.setCamMiddle()
        
    def setCamUp(self):
        self.pololu.setCamUp()
        
    def setCamDown(self):
        self.pololu.setCamDown()
        
    def readResistance(self):    
        self.microDue.readResistance()
        
    def rotateClockwise(self, angle):
        self.microDue.rotateClockwise(angle)
        self.angle = self.angle + angle
        
        if self.angle > 360:
            self.angle = self.angle - 360
        if self.angle < 0:
            self.angle = self.angle + 360
        
    def rotateCounterClockwise(self, angle):
        self.microDue.rotateCounterClockwise(angle)
        self.angle = self.angle - angle
        
        if self.angle > 360:
            self.angle = self.angle - 360
        if self.angle < 0:
            self.angle = self.angle + 360
        
    def rotateToAngle(self, angle):
        self.refreshAngle()
        if int(self.angle) != angle:
            deltaAngle = int(self.angle) - angle
            clockwise = (deltaAngle > 0)
            deltaAngle = abs(deltaAngle)
            if (deltaAngle > 180):
                clockwise = not clockwise
                deltaAngle = 360 - deltaAngle
            if clockwise:
                self.rotateClockwise(deltaAngle)
            else:
                self.rotateCounterClockwise(deltaAngle)
                
        #Update the angle in the robot, in case the robot need its last angle known        
        self.setAngle(angle)
        if self.angle > 360:
            self.angle = self.angle - 360
        if self.angle < 0:
            self.angle = self.angle + 360
        
    def grabPuck(self):     
        self.electromagnet.goDown()
        self.electromagnet.activate()
        self.electromagnet.goUp()
        
    def dropPuck(self):     
        self.electromagnet.goDown()
        self.electromagnet.desactivate()
        self.electromagnet.goUp()
    
    def waitForUpdateToFinish(self):
        lastUpdate = self.numberOfUpdates
        while self.numberOfUpdates == lastUpdate:
            time.sleep(0.1)
    
