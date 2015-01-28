# -*- coding: utf-8 -*-

from PIL import Image
from PIL import ImageTk
from Tkconstants import BOTH, SUNKEN, RIDGE
from Tkinter import Label, Button, Frame
import time
from main.GUI.GameBoard import GameBoard

class MainWindow(Frame):  
  
    def __init__(self, parent):
        
        def start():
            
            self.state = True
            self.timestart = time.time()

        def reset():
            self.buttonResetHasBeenPushed = True
        
        def stop():
            self.state = False   
            
        def finish():
            self.endstart = time.time()
            
        Frame.__init__(self, parent, background="white", borderwidth = 6, relief=SUNKEN) 
        self.gameBoard = GameBoard(self)  
        self.gameBoard.place(x=30, y=20)
        self.gameBoard.addSquare()
        
        self.timestart = 0
        self.endstart = 0
        self.state = False
        self.finished = False
        self.status = "Stopped"
        self.windowHasBeenClosed = False
        self.buttonResetHasBeenPushed = False
        self.startButton = Button(self, text="Start",command=start)
        self.startButton.config(height=1, width=15, font=("Helvetica", 22))
        self.startButton.place(x=430, y=45)
        
        self.stopButton = Button(self, text="Stop",command=stop)
        self.stopButton.config(height=1, width=15, font=("Helvetica", 22))
        self.stopButton.place(x=430, y=110)
        
        self.resetButton = Button(self, text="Reset", command=reset)
        self.resetButton.config(height=1, width=15, font=("Helvetica", 22))
        self.resetButton.place(x=430, y=172)
         
        self.parent = parent
        self.parent.title("Design III - Hello Kitty team")
        self.pack(fill=BOTH, expand=1)
        self.centerWindow()
        
        self.resistanceValueLabel = Label(self, text = "Undefined", font=("Times", "41", "bold italic"), bg = "white")
        self.resistanceValueLabel.place(x=452, y=475)
        
        self.timeValueLabel = Label(self, text = "Time : 0 ", font=("Times", "20", "bold italic"), bg = "white")
        self.timeValueLabel.place(x=422, y=565)
        
        self.statusLabel = Label(self, text = "Robot not started", font=("Times", "20", "bold italic"), bg = "white")
        self.statusLabel.place(x=422, y=600)     
        
        self.colorOneLabel = Label(self, text = "Undefined", font=("Helvetica", 24), relief=SUNKEN, bg="grey", borderwidth=3)
        self.colorOneLabel.configure(width=15)
        self.colorOneLabel.place(x=706, y=47)
        
        self.colorTwoLabel = Label(self, text = "Undefined", font=("Helvetica", 24), relief=SUNKEN, bg="grey", borderwidth=3)
        self.colorTwoLabel.configure(width=15)
        self.colorTwoLabel.place(x=706, y=112)
        
        self.colorThreeLabel = Label(self, text = "Undefined", font=("Helvetica", 24), relief=SUNKEN, bg="grey", borderwidth=3)
        self.colorThreeLabel.configure(width=15)
        self.colorThreeLabel.place(x=706, y=174)
        
        robotImage = Image.open("../../fig/robotBig.png")
        self.robotIcon = ImageTk.PhotoImage(robotImage)
        
        pathImage = Image.open("../../fig/path.png")
        self.pathIcon = ImageTk.PhotoImage(pathImage)
        
        letBo = Image.open("../../fig/LetterBoard.jpg")
        letBo = letBo.resize((190,190), Image.ANTIALIAS)
        letterBoard = ImageTk.PhotoImage(letBo)
        letterBoardLabel = Label(self, image=letterBoard, )
        letterBoardLabel.image = letterBoard
        letterBoardLabel.place(x=470, y=250)         

        sensBo = Image.open("../../fig/SensBoard.jpg")
        sensBo = sensBo.resize((190,190), Image.ANTIALIAS)
        sensBoard = ImageTk.PhotoImage(sensBo)
        orientationBoardLabel = Label(self, image=sensBoard)
        orientationBoardLabel.image = sensBoard
        orientationBoardLabel.place(x=745, y=250)
        
        tapepucks = Image.open("../../fig/TapeAndPucks.jpg")
        tapepucks = tapepucks.resize((220,220), Image.ANTIALIAS)
        tapeAndPucks = ImageTk.PhotoImage(tapepucks)
        squareLabel = Label(self, image=tapeAndPucks)
        squareLabel.image = tapeAndPucks
        squareLabel.place(x=740, y=449)
             
        self.puckCornerA = Label(self, text = "", relief=RIDGE, bg="RED", borderwidth=1)
        self.puckCornerA.configure(width=4, heigh=2)
        
        self.puckCornerB = Label(self, text = "", relief=RIDGE, bg="RED", borderwidth=1)
        self.puckCornerB.configure(width=4, heigh=2)
        
        self.puckCornerC = Label(self, text = "", relief=RIDGE, bg="RED", borderwidth=1)
        self.puckCornerC.configure(width=4, heigh=2)
        
        self.puckCornerD = Label(self, text = "", relief=RIDGE, bg="RED", borderwidth=1)
        self.puckCornerD.configure(width=4, heigh=2)

        self.letterReadLabel = Label(self,font=("Helvetica", 30), text = "Z", bg="white", borderwidth=0)
        self.positionReadLabel = Label(self,font=("Helvetica", 30), text = "ZZ", bg="WHITE", borderwidth=0)        
                
    def centerWindow(self):
        w = 1070
        h = 690

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        
        x = (sw - w)/2
        y = (sh - h - 55)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

        