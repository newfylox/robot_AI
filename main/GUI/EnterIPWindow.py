from Tkinter import Entry
import Tkinter


class EnterIPWindow(object):
    
    def __init__(self):
        self.serverAddress = 0
        self.setWindow()
        self.setEntryInput()
        self.setButtonOK()
        self.root.mainloop()
        
    def setWindow(self):
        self.root = Tkinter.Tk()
        windowWidth = 300
        windowHeight = 50
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()
        xPosition = (screenWidth / 2) - (windowWidth / 2)
        yPosition = (screenHeight / 2) - (windowHeight / 2)
        self.root.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, xPosition, yPosition))
        self.root.title("Server IP Address")
        self.root.bind('<Return>', self.hitEnter)
        self.root.bind('<KP_Enter>', self.hitEnter)
        
    def setEntryInput(self):
        self.textInput = Entry(self.root)
        self.textInput.focus()
        self.textInput.pack()
        
    def setButtonOK(self):
        self.button = Tkinter.Button(self.root, text='OK', command=self.closeWindow)
        self.button.pack()
        
    def closeWindow(self, event=None):
        self.serverAddress = self.textInput.get()
        self.root.destroy()
        self.root.quit()
        
    def hitEnter(self, event):
        self.closeWindow(event)
