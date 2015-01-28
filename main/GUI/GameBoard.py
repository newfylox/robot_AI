import Tkinter as tk

class GameBoard(tk.Frame):
    def __init__(self, parent, rows=46, columns=23, squareSize=15, color1="white", color2="white"):

        self.rows = rows
        self.columns = columns
        self.squareSize = squareSize
        self.color1 = color1
        self.color2 = color2
        self.pieces = {}
        self.numberOfPathSquare = 0
        
        canvasWidth = columns * squareSize
        canvasHeight = rows * squareSize

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvasWidth, height=canvasHeight)
        self.canvas.pack(side="top", fill="both", expand=True, padx=0, pady=0)

        self.canvas.bind("<Configure>", self.refresh)
        
    def addObstacle(self, name, obstacleCoords):
        x0 = (obstacleCoords[1] * self.squareSize) -(4*self.squareSize)
        y0 = (obstacleCoords[0] * self.squareSize) -(4*self.squareSize)
        x1 = x0 + (9*self.squareSize)
        if x1 > self.squareSize*self.columns:
            x1 = self.squareSize*self.columns
        y1 = y0 + (9*self.squareSize)
        if y1 > self.squareSize*self.rows:
            y1 = self.squareSize*self.rows
        self.canvas.create_rectangle(x0,y0,x1,y1,fill="red",tags=(name, "piece"), outline="")
        self.placePieceObstacle(name, obstacleCoords[0], obstacleCoords[1])
        
    def addPuck(self, name, obstacleCoords):
        x0 = (obstacleCoords[1] * self.squareSize)
        y0 = (obstacleCoords[0] * self.squareSize)
        x1 = x0 + (1*self.squareSize)
        y1 = y0 + (1*self.squareSize)
        self.canvas.create_rectangle(x0,y0,x1,y1,fill=name.replace("p-",""),tags=(name, "piece"), outline="")
        self.placePiecePuck(name, obstacleCoords[0], obstacleCoords[1])
        
    def addSquare(self, name="greensquare", coords = (4,4)):
        x0 = (coords[1] * self.squareSize)
        y0 = (coords[0] * self.squareSize)
        x1 = x0 + (13*self.squareSize)
        y1 = y0 + (13*self.squareSize)
        self.canvas.create_rectangle(x0,y0,x1,y1,fill="",tags=(name, "piece"), outline="green", width=5)
        self.placePieceSquare(name, coords[0], coords[1])

    def addPath(self, aPath, image):
        if self.numberOfPathSquare > 0:
            i = 0
            while i < self.numberOfPathSquare:
                self.canvas.delete("path"+str(i+1))
                i = i + 1
            self.numberOfPathSquare = 0
        for coords in aPath:
            self.numberOfPathSquare = self.numberOfPathSquare + 1
            coords = (int(coords.split(",")[0]),int(coords.split(",")[1]))
            self.addPiece("path" + str(self.numberOfPathSquare), image, coords[0], coords[1])
        

    def addPiece(self, name, image, row=0, column=0):
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.placePiece(name, row, column)

    def placePiece(self, name, row, column):
        self.pieces[name] = (row, column)
        x0 = (column * self.squareSize) + int(self.squareSize/2)
        y0 = (row * self.squareSize) + int(self.squareSize/2)
        self.canvas.coords(name, x0, y0)
        
    def placePieceObstacle(self, name, x0, y0):
        self.pieces[name] = (x0, y0)
        a = (y0 * self.squareSize) -(4*self.squareSize)
        b = (x0 * self.squareSize) -(4*self.squareSize)
        c = a + (9*self.squareSize)
        if c > self.squareSize*self.columns:
            c = self.squareSize*self.columns
        d = b + (9*self.squareSize)
        if d > self.squareSize*self.rows:
            d = self.squareSize*self.rows
        self.canvas.coords(name, a, b, c, d)
        
    def placePiecePuck(self, name, x0, y0):
        self.pieces[name] = (x0, y0)
        a = (y0 * self.squareSize)
        b = (x0 * self.squareSize)
        c = a + (1*self.squareSize)
        d = b + (1*self.squareSize)
        self.canvas.coords(name, a, b, c, d)
        
    def placePieceSquare(self, name, x0, y0):
        self.pieces[name] = (x0, y0)
        a = (y0 * self.squareSize)
        b = (x0 * self.squareSize)
        c = a + (13*self.squareSize)
        d = b + (13*self.squareSize)
        self.canvas.coords(name, a, b, c, d)

    def refresh(self, event):
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.squareSize = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.squareSize)
                y1 = (row * self.squareSize)
                x2 = x1 + self.squareSize
                y2 = y1 + self.squareSize
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            if "obstacle" in name:
                self.placePieceObstacle(name, self.pieces[name][0], self.pieces[name][1])
            elif "p-" in name:
                self.placePiecePuck(name, self.pieces[name][0], self.pieces[name][1])
            elif "greensquare" in name:
                self.placePieceSquare(name, self.pieces[name][0], self.pieces[name][1])
            else:
                self.placePiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")
