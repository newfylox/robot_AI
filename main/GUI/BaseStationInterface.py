#!/usr/bin/python
# -*- coding: utf-8 -*-

from main.GUI.MainWindow import MainWindow
import time

class BaseStationInterface():
    def __init__(self, root):
        self.root = root
        self.mainWindow = MainWindow(self.root) 
        self.mainWindow.centerWindow() 
            
        self.textColorOne = "grey"              
        self.textColorTwo = "grey" 
        self.textColorThree = "grey" 
        
        self.textCornerAColor = "grey"              
        self.textCornerBColor = "grey" 
        self.textCornerCColor = "grey" 
        self.textCornerDColor = "grey" 
        
        self.puckCornerAVisible = False
        self.puckCornerBVisible = False
        self.puckCornerCVisible = False
        self.puckCornerDVisible = False
        self.status = "Robot not started"
        
        self.resistanceValueLabel = 0  
        
        self.textLetterBoard = " "
        self.positionXLetterBoard = 0 
        self.positionYLetterBoard = 0 

        self.textOrientationBoard = " "
        self.positionXOrientationBoard = 0 
        self.positionYOrientationBoard = 0 
              
        self.root.after(10, self.updateLabels)
     
    def updateLabels(self):
        self.mainWindow.colorOneLabel.configure(bg=self.textColorOne, text=self.textColorOne)
        self.mainWindow.colorTwoLabel.configure(bg=self.textColorTwo, text=self.textColorTwo)    
        self.mainWindow.colorThreeLabel.configure(bg=self.textColorThree, text=self.textColorThree)  
        self.mainWindow.resistanceValueLabel.configure(text=str(self.resistanceValueLabel) + " Ω")
        self.mainWindow.statusLabel.configure(text=str(self.status))
        self.mainWindow.puckCornerA.configure(bg=self.textCornerAColor)
        self.mainWindow.puckCornerB.configure(bg=self.textCornerBColor)
        self.mainWindow.puckCornerC.configure(bg=self.textCornerCColor)
        self.mainWindow.puckCornerD.configure(bg=self.textCornerDColor)     
        self.mainWindow.letterReadLabel.place(x=self.positionXLetterBoard, y=self.positionYLetterBoard)
        self.mainWindow.letterReadLabel.configure(text=self.textLetterBoard)
        self.mainWindow.positionReadLabel.place(x=self.positionXOrientationBoard, y=self.positionYOrientationBoard)
        self.mainWindow.positionReadLabel.configure(text=self.textOrientationBoard)
        
        if self.mainWindow.finished == True:
            startTime = int(self.mainWindow.timestart)
            endTime = int(time.time())
            stringTime = "Time : " + str(endTime - startTime) + " seconds"
            self.mainWindow.timeValueLabel.configure(text=stringTime)
            
        if self.puckCornerAVisible == True:
            self.mainWindow.puckCornerA.place(x=750, y=460)
        else:
            self.mainWindow.puckCornerA.place(x=999, y=999)
            
        if self.puckCornerBVisible == True:
            self.mainWindow.puckCornerB.place(x=917, y=460)
        else:
            self.mainWindow.puckCornerB.place(x=999, y=999)
            
        if self.puckCornerCVisible == True:
            self.mainWindow.puckCornerC.place(x=917, y=630)
        else:
            self.mainWindow.puckCornerC.place(x=999, y=999)
                        
        if self.puckCornerDVisible == True:
            self.mainWindow.puckCornerD.place(x=749, y=630)
        else:
            self.mainWindow.puckCornerD.place(x=999, y=999)
        