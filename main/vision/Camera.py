import cv2
import numpy as np

class Camera(object):

    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.xDistBetweenDotAndRobot = -6
        self.yDistBetweenDotAndRobot = 30
        self.calibrationMatrix = np.array([[  2.49689609e+02,   6.33448461e+02,   1.86519782e+02, 1.13577674e+04],[ -2.78452467e+02,  1.48113071e+01,   6.80048369e+02, 1.81283534e+04],[  7.82249601e-01,  1.96791379e-02,  6.22654233e-01,4.63801565e+01]])
        #threasholdValue
        #0BlackColor
        self.H_MINBlack = 0
        self.S_MINBlack = 0
        self.V_MINBlack = 0
        self.H_MAXBlack = 255
        self.S_MAXBlack = 255
        self.V_MAXBlack = 34
        #1BrownColor
        self.H_MINBrown = 5
        self.S_MINBrown = 95
        self.V_MINBrown = 0
        self.H_MAXBrown = 27
        self.S_MAXBrown = 255
        self.V_MAXBrown = 202
        #2RedColor
        self.H_MINRed = 0
        self.S_MINRed = 161
        self.V_MINRed = 20
        self.H_MAXRed = 8
        self.S_MAXRed = 255
        self.V_MAXRed = 255
        #3OrangeColor
        self.H_MINOrange = 4
        self.S_MINOrange = 85
        self.V_MINOrange = 144
        self.H_MAXOrange = 19
        self.S_MAXOrange = 255
        self.V_MAXOrange = 255
        #4YellowColor
        self.H_MINYellow = 23
        self.S_MINYellow = 164
        self.V_MINYellow = 62
        self.H_MAXYellow = 31
        self.S_MAXYellow = 255
        self.V_MAXYellow = 255
        #5GreenColor
        self.H_MINGreen = 52
        self.S_MINGreen = 89
        self.V_MINGreen = 47
        self.H_MAXGreen = 74
        self.S_MAXGreen = 255
        self.V_MAXGreen = 255
        #GreenContourColor
        self.H_MINGreenContour = 53
        self.S_MINGreenContour = 60
        self.V_MINGreenContour = 24
        self.H_MAXGreenContour = 73
        self.S_MAXGreenContour = 255
        self.V_MAXGreenContour = 255
        #6BlueColor
        self.H_MINBlue = 100
        self.S_MINBlue = 56
        self.V_MINBlue = 42
        self.H_MAXBlue = 116
        self.S_MAXBlue = 255
        self.V_MAXBlue = 255
        #CyanColor
        self.H_MINCyan = 67
        self.S_MINCyan = 25
        self.V_MINCyan = 90
        self.H_MAXCyan = 87
        self.S_MAXCyan = 215
        self.V_MAXCyan = 255
        #7PurpleColor
        self.H_MINPurple = 2
        self.S_MINPurple = 0
        self.V_MINPurple = 60
        self.H_MAXPurple = 28
        self.S_MAXPurple = 52
        self.V_MAXPurple = 205
        #8GrayColor
        self.H_MINGray = 19
        self.S_MINGray = 153
        self.V_MINGray = 0
        self.H_MAXGray = 25
        self.S_MAXGray= 255
        self.V_MAXGray = 254
        #9WhiteColor
        self.H_MINWhite = 16
        self.S_MINWhite = 18
        self.V_MINWhite = 170
        self.H_MAXWhite = 48
        self.S_MAXWhite = 123
        self.V_MAXWhite = 255
     
    #return one frame
    def getImage(self):
        #img = cv2.imread('tab.png')
        for i in range(0,10):  # @UnusedVariable
            ret, img = self.camera.read() # @UnusedVariable
        return img
    
    #find the good square 
    def squareDetection(self, image, position):
        #make an black and white threshold
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)        
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2) 
    
        #find the biggest contour
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        max_area = 0
        for i in contours:
            area = cv2.contourArea(i)
            if area > 100:
                peri = cv2.arcLength(i, True)
                approx = cv2.approxPolyDP(i, 0.02 * peri, True)
                if area > max_area and len(approx) == 4:
                    max_area = area
                    cnt = i
        
        if max_area < 20000:
            return None, None, None, None, None
        # find the four corner of the square
        height, width, ch = image.shape  # @UnusedVariable
        img = np.zeros((height,width,3), np.uint8)
        img[:,:] = (255,255,255)
        cv2.drawContours(img,[cnt],-1,(0,0,0),20)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)        
        corners = cv2.goodFeaturesToTrack(gray,4,0.2,100)
        corners = np.int0(corners)
        listPoints = []
        for i in corners:
            x,y = i.ravel()
            cv2.circle(img,(x,y),5,(0,255,0),-1)
            listPoints.append((x,y))
        
        pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
        #tidy up the corner
        compMax = listPoints[0][0]+listPoints[0][1]
        compMin = compMax
        p1 = listPoints[0]
        p4 = listPoints[0]
        for i in range(len(listPoints)):
            if listPoints[i][0]+listPoints[i][1]>compMax:
                compMax = listPoints[i][0]+listPoints[i][1]
                p4 = listPoints[i]
            if listPoints[i][0]+listPoints[i][1]<compMin:
                compMin = listPoints[i][0]+listPoints[i][1]
                p1 = listPoints[i]
        listPoints.remove(p1)
        listPoints.remove(p4)
        if listPoints[0][0]>listPoints[1][0]:
            p3 = listPoints[1]
            p2 = listPoints[0]
        else:
            p3 = listPoints[0]
            p2 = listPoints[1]
        #make perspective   
        pts1 = np.float32([p1,p2,p3,p4])
        M = cv2.getPerspectiveTransform(pts1,pts2)
        img = cv2.warpPerspective(image,M,(width,height))
        
        #find the 3X3 size in the square
        x1 = 0
        x2 = width/3 
        x3 = 2*width/3
        x4 = width
        y1 = 0
        y2 = height/3
        y3 = 2*height/3
        y4 = height
        
        #find all 16 intersection
        p1 = (x1, y1)
        p2 = (x2, y1)
        p3 = (x3, y1)
        p4 = (x4, y1)
        p5 = (x1, y2)
        p6 = (x2, y2)
        p7 = (x3, y2)
        p8 = (x4, y2)
        p9 = (x1, y3)
        p10 = (x2, y3)
        p11 = (x3, y3)
        p12 = (x4, y3)
        p13 = (x1, y4)
        p14 = (x2, y4)
        p15 = (x3, y4)
        p16 = (x4, y4)
        
        #return the 4 point of the good position
        if position == 1:
            return p1, p2, p5, p6, img
        elif position == 2:
            return p2, p3, p6, p7, img
        elif position == 3:
            return p3, p4, p7, p8, img
        elif position == 4:
            return p5, p6, p9, p10, img
        elif position == 5:
            return p6, p7, p10, p11, img
        elif position == 6:
            return p7, p8, p11, p12, img
        elif position == 7:
            return p9, p10, p13, p14, img
        elif position == 8:
            return p10, p11, p14, p15, img
        elif position == 9:
            return p11, p12, p15, p16, img
        
        
    # return the good letter 
    def findLetterInLetterBoard(self, position):
        #get a frame
        image = self.getImage()
        #find the good square by his position
        p1, p2, p3, p4, image = self.squareDetection(image, position)
        if p1 == None or p2 == None or p3 == None or p4 == None or image == None:
            return None
        #print p1,p2,p3,p4
        #read the template
        A = cv2.imread('../../fig/A.png')
        B = cv2.imread('../../fig/B.png')
        C = cv2.imread('../../fig/C.png')
        D = cv2.imread('../../fig/D.png')
        #A = cv2.imread('A.png')
        #B = cv2.imread('B.png')
        #C = cv2.imread('C.png')
        #D = cv2.imread('D.png')
        
        #call of the match function for all letter, return the number of point in the good letter 
        cptA = self.match(image, A, p1, p2, p3, p4)  # @UnusedVariable
        cptB = self.match(image, B, p1, p2, p3, p4)  # @UnusedVariable
        cptC = self.match(image, C, p1, p2, p3, p4)  # @UnusedVariable
        cptD = self.match(image, D, p1, p2, p3, p4)  # @UnusedVariable
        
        #print cptA, cptB, cptC, cptD
        #return the maximum letter
        if cptA > cptB and cptA > cptC and cptA > cptD:
            return 'A'
        elif cptB > cptA and cptB > cptC and cptB > cptD:
            return 'B'
        elif cptC > cptB and cptC > cptA and cptC > cptD:
            return 'C'
        elif cptD > cptB and cptD > cptC and cptD > cptA:
            return 'D'
        else:
            return None
        
    def findOrientationInOrientationBoard(self, position):
        #get a frame
        image = self.getImage()
        #find a square by his position
        p1, p2, p3, p4, image = self.squareDetection(image, position)
        #read template
        SH = cv2.imread('../../fig/SH.png')
        SA = cv2.imread('../../fig/SA.png')
        #SH = cv2.imread('SH.png')
        #SA = cv2.imread('SA.png')
        #call of the match function for all letter, return the number of point in the good letter
        cptSH = self.match(image, SH, p1, p2, p3, p4)  # @UnusedVariable
        cptSA = self.match(image, SA, p1, p2, p3, p4)  # @UnusedVariable
 
        #return the maximal letter
        if cptSH > cptSA:
            return 'SH'
        elif cptSA > cptSH:
            return 'SA'
        else:
            return None
    
    #template matching 
    def match(self, image, lettre, p1, p2, p3, p4):
        #perform a blur on the frame
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        lettre_gray = cv2.cvtColor(lettre, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (7, 7), 0)
        lettre_blur = cv2.GaussianBlur(lettre_gray, (7, 7), 0)
        w, h, prof = lettre.shape[::-1] # @UnusedVariable
        #self.show(img_blur)
        #self.show(lettre_blur)
        #template matching function
        res = cv2.matchTemplate(img_blur, lettre_blur, cv2.TM_CCOEFF_NORMED)
        loc = np.where( res >= 0.8)
        cpt = 0
        
        for pt in zip(*loc[::-1]):
            if pt[0] > p1[0] and pt[0] > p3[0] and pt[0] < p2[0] and pt[0] < p4[0]:
                if pt[1] > p1[1] and pt[1] > p2[1] and pt[1] < p3[1] and pt[1] < p4[1]:
                    cpt = cpt + 1
        #return the number of point on the letter
        return cpt
    
    def show(self, img):
        while(1):
            cv2.imshow('Affichage', img)  
            cc = cv2.waitKey(10)
            if cc == 27: # Touche Echap quitte
                break
            
    def getColorArray(self,colorCode):  
        if colorCode == 0:
            colorMin = np.array([self.H_MINBlack, self.S_MINBlack, self.V_MINBlack],np.uint8)
            colorMax = np.array([self.H_MAXBlack, self.S_MAXBlack, self.V_MAXBlack],np.uint8)
        if colorCode == 1: 
            colorMin = np.array([self.H_MINBrown, self.S_MINBrown, self.V_MINBrown],np.uint8)
            colorMax = np.array([self.H_MAXBrown, self.S_MAXBrown, self.V_MAXBrown],np.uint8)
        if colorCode == 2:
            colorMin = np.array([self.H_MINRed, self.S_MINRed, self.V_MINRed],np.uint8)
            colorMax = np.array([self.H_MAXRed, self.S_MAXRed, self.V_MAXRed],np.uint8)
        if colorCode == 3:
            colorMin = np.array([self.H_MINOrange, self.S_MINOrange, self.V_MINOrange],np.uint8)
            colorMax = np.array([self.H_MAXOrange, self.S_MAXOrange, self.V_MAXOrange],np.uint8)
        if colorCode == 4:
            colorMin = np.array([self.H_MINYellow, self.S_MINYellow, self.V_MINYellow],np.uint8)
            colorMax = np.array([self.H_MAXYellow, self.S_MAXYellow, self.V_MAXYellow],np.uint8)
        if colorCode == 5:   
            colorMin = np.array([self.H_MINGreen, self.S_MINGreen, self.V_MINGreen],np.uint8)
            colorMax = np.array([self.H_MAXGreen, self.S_MAXGreen, self.V_MAXGreen],np.uint8) 
        if colorCode == 6:
            colorMin = np.array([self.H_MINBlue, self.S_MINBlue, self.V_MINBlue],np.uint8)
            colorMax = np.array([self.H_MAXBlue, self.S_MAXBlue, self.V_MAXBlue],np.uint8) 
        if colorCode == 7:
            colorMin = np.array([self.H_MINPurple, self.S_MINPurple, self.V_MINPurple],np.uint8)
            colorMax = np.array([self.H_MAXPurple, self.S_MAXPurple, self.V_MAXPurple],np.uint8) 
        if colorCode == 8:
            colorMin = np.array([self.H_MINGray, self.S_MINGray, self.V_MINGray],np.uint8)
            colorMax = np.array([self.H_MAXGray, self.S_MAXGray, self.V_MAXGray],np.uint8) 
        if colorCode == 9: 
            colorMin = np.array([self.H_MINWhite, self.S_MINWhite, self.V_MINWhite],np.uint8)
            colorMax = np.array([self.H_MAXWhite, self.S_MAXWhite, self.V_MAXWhite],np.uint8) 
        return colorMin,colorMax
    
    def thesholdForASpecificColor(self,Color_Min,Color_Max):  
        ParamErode = 3
        frame = self.getImage()
        element = cv2.getStructuringElement(cv2.MORPH_CROSS,(ParamErode,ParamErode))
        frame_hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_blur = cv2.GaussianBlur(frame_hsv ,(5,5),0)
        frame_threshed = cv2.inRange(frame_blur, Color_Min, Color_Max)
        frame_erode = cv2.erode(frame_threshed ,element,iterations = 3)
        frame_dilate = cv2.dilate(frame_erode,element,iterations = 3)
        frame_dilate2 = cv2.dilate(frame_dilate,element,iterations = 20)
        frame_final = cv2.erode(frame_dilate2,element,iterations = 20) 
        return frame_final  
    
    def getRealPuckDistanceToRobot(self,uPos,vPos):
        u = uPos
        v = vPos
        m = self.calibrationMatrix
        YDistToDotNum = (-m[0][3]+u*m[2][3])*(m[1][1]-v*m[2][1]) - (m[1][3]-v*m[2][3])*(-m[0][1]+u*m[2][1])
        YDistToDotDenum = (m[0][0]-u*m[2][0])*(m[1][1]-v*m[2][1]) + (m[0][1]-u*m[2][1])*(-m[1][0]+v*m[2][0])
        YDistToDot = YDistToDotNum/YDistToDotDenum
        XDistToDotNum = (-m[0][3]+u*m[2][3])*(-m[1][0]+v*m[2][0]) - (m[1][3]-v*m[2][3])*(m[0][0]-u*m[2][0])
        XDistToDotDenum = (m[0][0]-u*m[2][0])*(m[1][1]-v*m[2][1]) + (m[0][1]-u*m[2][1])*(-m[1][0]+v*m[2][0])
        XDistToDot = XDistToDotNum/XDistToDotDenum
        XDistToRobot = XDistToDot + self.xDistBetweenDotAndRobot
        YDistToRobot = YDistToDot + self.yDistBetweenDotAndRobot
        hypothenuseDistance = np.sqrt(XDistToRobot*XDistToRobot +(YDistToRobot-10)*(YDistToRobot-10))
        if YDistToRobot >= 0:
            angleRotation = np.rad2deg(np.arctan(XDistToRobot/YDistToRobot))
        return angleRotation , hypothenuseDistance
    
    def getRealCornerDistanceToRobot(self,uPos,vPos):
        u = uPos
        v = vPos
        m = self.calibrationMatrix
        YDistToDotNum = (-m[0][3]+u*m[2][3])*(m[1][1]-v*m[2][1]) - (m[1][3]-v*m[2][3])*(-m[0][1]+u*m[2][1])
        YDistToDotDenum = (m[0][0]-u*m[2][0])*(m[1][1]-v*m[2][1]) + (m[0][1]-u*m[2][1])*(-m[1][0]+v*m[2][0])
        YDistToDot = YDistToDotNum/YDistToDotDenum
        yDistToRobot = YDistToDot + self.yDistBetweenDotAndRobot - 12
        return yDistToRobot
    
    def findSquareCorner(self):  
        colorMin = np.array([self.H_MINGreenContour, self.S_MINGreenContour, self.V_MINGreenContour],np.uint8)
        colorMax = np.array([self.H_MAXGreenContour, self.S_MAXGreenContour, self.V_MAXGreenContour],np.uint8)
        Frame_final = self.thesholdForASpecificColor(colorMin, colorMax)
        frame = self.getImage()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        Frame_melange_gray_threshold = cv2.bitwise_and(gray,gray, mask = Frame_final)
        edges = cv2.Canny(Frame_melange_gray_threshold,50,150,apertureSize = 3)
        #Last parameter is the minimal lenght acceppted
        lines = cv2.HoughLines(edges,1,np.pi/180,100)
        if not((lines == None) or not(lines.size)):
            count = 0
            Droite = list()
            DroitePositive = list()
            DroiteNegative = list()
            BiggestDroite = list()
            SmallestDroite = list()
            Intersection1 = list()
            Intersection2 = list()
            for rho,theta in lines[0]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                #find  mx + b
                if(x2-x1)==0:
                    m = 0
                else:
                    m = float((y2-y1))/(x2-x1)
                b = y1 - m*x1
                Droite.append((m,b))
                count += 1  
            if count >= 2:
                for i in range(0,len(Droite)):
                    if Droite[i][0] >= 0:
                        DroitePositive.append(Droite[i])
                    else:
                        DroiteNegative.append(Droite[i]) 
                if len(DroitePositive) >= 2 and len(DroiteNegative) >= 2:
                    if DroitePositive[0][1] >= DroitePositive[1][1]:
                        BiggestDroite.append(DroitePositive[0]) 
                        SmallestDroite.append(DroitePositive[1])
                    else:
                        BiggestDroite.append(DroitePositive[1])
                        SmallestDroite.append(DroitePositive[0])
                    if DroiteNegative[0][1] >= DroiteNegative[1][1]:
                        BiggestDroite.append(DroiteNegative[0])
                        SmallestDroite.append(DroiteNegative[1])
                    else:
                        BiggestDroite.append(DroiteNegative[1])  
                        SmallestDroite.append(DroiteNegative[0])         
                    m1 = BiggestDroite[0][0]
                    b1 = BiggestDroite[0][1]
                    m2 = BiggestDroite[1][0]
                    b2 = BiggestDroite[1][1]
                    Intersection1.append((b2-b1)/(m1-m2))
                    Intersection1.append((m1*Intersection1[0] + b1))
                    m3 = SmallestDroite[0][0]
                    b3 = SmallestDroite[0][1]
                    m4 = SmallestDroite[1][0]
                    b4 = SmallestDroite[1][1]
                    Intersection2.append((b4-b3)/(m3-m4))
                    Intersection2.append((m3*Intersection2[0] + b3))
                    Middlex = (Intersection1[0]+Intersection2[0])/2
                    Middley = (Intersection1[1]+Intersection2[1])/2
                    return(Middlex,Middley)
                elif len(DroitePositive) >= 1 and len(DroiteNegative) >= 1:
                    m1 = DroitePositive[0][0]
                    b1 = DroitePositive[0][1]
                    m2 = DroiteNegative[0][0]
                    b2 = DroiteNegative[0][1]
                    Intersection1.append((b2-b1)/(m1-m2))
                    Intersection1.append((m1*Intersection1[0] + b1)) 
                    return (Intersection1[0],Intersection1[1])
        #if not found
        return -1,-1
    
    def getDistanceToCorner(self):
        cornerX,cornerY = self.findSquareCorner()
        if cornerX == -1 or cornerY == -1:
            return -1
        robotDistanceToCorner = self.getRealCornerDistanceToRobot(cornerX, cornerY) 
        return robotDistanceToCorner
    
    
    def isPuckPlaced(self,puckColorCode):
        #return 0 if ok
        #return 1 if not ok
        #return -1 si error
        #upgrade the maxerror make the fonction less accurate 
        maxError = 30
        middlex,middley = self.findSquareCorner()
        if middlex == -1 or middley == -1:
            return -1
        PuckPositionx,PuckPositiony = self.findColor(puckColorCode)
        if PuckPositionx == -1 or PuckPositiony == -1:
            return -1
        if np.abs(PuckPositionx - middlex) < maxError and np.abs(PuckPositiony - middley) < maxError:
            return 1
        else:
            return 0
        
    def getDistanceToPuck(self,colorCode):
        positionx,positiony = self.findColor(colorCode)
        if positionx == -1 or positiony == -1:
            return -1,-1
        rotationAngleNeeded , robotDistanceToPuck = self.getRealPuckDistanceToRobot(positionx, positiony)
        return rotationAngleNeeded,robotDistanceToPuck
    
    def findColor(self,colorCode):
        if colorCode == 0:
            positionx,positiony = self.findBlackPuck()
        if colorCode == 1: 
            positionx,positiony = self.findBrownPuck()
        if colorCode == 2:
            positionx,positiony = self.findRedPuck()
        if colorCode == 3:
            positionx,positiony = self.findOrangePuck()
        if colorCode == 4:
            positionx,positiony = self.findYellowPuck()
        if colorCode == 5:   
            positionx,positiony = self.findGreenPuck()    
        if colorCode == 6:
            positionx,positiony = self.findBluePuck()
        if colorCode == 7:
            positionx,positiony = self.findPurplePuck()
        if colorCode == 8:
            positionx,positiony = self.findGrayPuck()
        if colorCode == 9: 
            positionx,positiony = self.findWhitePuck()
        return positionx,positiony               

    def findBluePuck(self):     
        color_min_blue = np.array([self.H_MINBlue, self.S_MINBlue, self.V_MINBlue],np.uint8)
        color_max_blue = np.array([self.H_MAXBlue, self.S_MAXBlue, self.V_MAXBlue],np.uint8)  
        Img_Threshed_Blue = self.thesholdForASpecificColor(color_min_blue, color_max_blue) 
        positionBlueAndBrownx, positionBlueAndBrowny = self.findBrownPuck()
        if positionBlueAndBrownx != -1:
            DiscardSize = 80
            xmin = positionBlueAndBrownx - DiscardSize
            ymin = positionBlueAndBrowny - DiscardSize
            xmax = positionBlueAndBrownx + DiscardSize
            ymax = positionBlueAndBrowny + DiscardSize
            if xmin < 0 :
                xmin = 0
            if ymin < 0:
                ymin = 0
            Img_Threshed_Blue[ymin:ymax,xmin:xmax] = 0
            contour_Blue,_ = cv2.findContours( Img_Threshed_Blue, mode=cv2.RETR_LIST,method=cv2.CHAIN_APPROX_SIMPLE )
            _ = np.zeros(Img_Threshed_Blue.shape[0:2])
            _ = np.zeros(Img_Threshed_Blue.shape[0:2])
            bigestPerimeter = 0
            largest_Contour = 0
            find_One_Contour = False
            if (contour_Blue):
                for i in range(len(contour_Blue)):
                    individual_Contour_Blue = contour_Blue[i - 1]
                    perimeter = cv2.arcLength(individual_Contour_Blue,True)
                    if perimeter > bigestPerimeter:
                        bigestPerimeter = perimeter
                        largest_Contour = individual_Contour_Blue
                        find_One_Contour = True
                individual_Contour_Blue = largest_Contour    
                mass_Of_Blue_Puck = cv2.moments(individual_Contour_Blue)
                if (find_One_Contour):
                    if mass_Of_Blue_Puck['m00'] != 0:  
                        centerOfMass = ( mass_Of_Blue_Puck['m10']/mass_Of_Blue_Puck['m00'],mass_Of_Blue_Puck['m01']/mass_Of_Blue_Puck['m00'] )
                        (position_Pixel_x,position_Pixel_y) = centerOfMass
                        return (position_Pixel_x,position_Pixel_y)
        #if not found
        return -1,-1   
    
    def findGreenPuck(self):
        color_min_green = np.array([self.H_MINGreen, self.S_MINGreen, self.V_MINGreen],np.uint8)
        color_max_green = np.array([self.H_MAXGreen, self.S_MAXGreen, self.V_MAXGreen],np.uint8)  
        img_Threshed_Green = self.thesholdForASpecificColor(color_min_green, color_max_green)
        contour_Green,_ = cv2.findContours( img_Threshed_Green, mode=cv2.RETR_LIST,method=cv2.CHAIN_APPROX_SIMPLE )
        _ = np.zeros(img_Threshed_Green.shape[0:2])
        _ = np.zeros(img_Threshed_Green.shape[0:2])
        bigestPerimeter = 0
        largest_Contour = 0
        find_One_Contour = False
        if (contour_Green):
            for i in range(len(contour_Green)):
                individual_Contour_Green = contour_Green[i - 1]
                perimeter = cv2.arcLength(individual_Contour_Green,True)
                if perimeter > bigestPerimeter:
                    bigestPerimeter = perimeter
                    largest_Contour = individual_Contour_Green
                    find_One_Contour = True
            individual_Contour_Green = largest_Contour    
            massOfGreenPuck = cv2.moments(individual_Contour_Green)
            if (find_One_Contour):
                if massOfGreenPuck['m00'] != 0:  
                    centerOfMass = ( massOfGreenPuck['m10']/massOfGreenPuck['m00'],massOfGreenPuck['m01']/massOfGreenPuck['m00'] )
                    (position_Pixel_x,position_Pixel_y) = centerOfMass
                    return (position_Pixel_x,position_Pixel_y)
        #if not found
        return -1,-1  
    
    def findYellowPuck(self):
        color_min_yellow = np.array([self.H_MINYellow, self.S_MINYellow, self.V_MINYellow],np.uint8)
        color_max_yellow = np.array([self.H_MAXYellow, self.S_MAXYellow, self.V_MAXYellow],np.uint8)  
        Img_Threshed_Yellow = self.thesholdForASpecificColor(color_min_yellow, color_max_yellow)
        Contour_Yellow,_ = cv2.findContours( Img_Threshed_Yellow, mode=cv2.RETR_LIST,method=cv2.CHAIN_APPROX_SIMPLE )
        _ = np.zeros(Img_Threshed_Yellow.shape[0:2])
        _ = np.zeros(Img_Threshed_Yellow.shape[0:2])
        BigestPerimeter = 0
        Largest_Contour = 0
        Find_One_Contour = False
        if (Contour_Yellow):
            for i in range(len(Contour_Yellow)):
                Individual_Contour_Yellow = Contour_Yellow[i - 1]
                Perimeter = cv2.arcLength(Individual_Contour_Yellow,True)
                if Perimeter > BigestPerimeter:
                    BigestPerimeter = Perimeter
                    Largest_Contour = Individual_Contour_Yellow
                    Find_One_Contour = True
            Individual_Contour_Yellow = Largest_Contour    
            Mass_Of_Yellow_Puck = cv2.moments(Individual_Contour_Yellow)
            if (Find_One_Contour):
                if Mass_Of_Yellow_Puck['m00'] != 0:  
                    Center_Of_The_Mass = ( Mass_Of_Yellow_Puck['m10']/Mass_Of_Yellow_Puck['m00'],Mass_Of_Yellow_Puck['m01']/Mass_Of_Yellow_Puck['m00'] )
                    (Position_Pixel_x,Position_Pixel_y) = Center_Of_The_Mass
                    return (Position_Pixel_x,Position_Pixel_y)
        #if not found
        return -1,-1   
    
    def findBrownPuck(self):
        color_min_blue = np.array([self.H_MINBlue, self.S_MINBlue, self.V_MINBlue],np.uint8)
        color_max_Blue = np.array([self.H_MAXBlue, self.S_MAXBlue, self.V_MAXBlue],np.uint8)  
        ParamErode = 3
        frame = self.getImage()
        element = cv2.getStructuringElement(cv2.MORPH_CROSS,(ParamErode,ParamErode))
        frame_hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_blur = cv2.GaussianBlur(frame_hsv ,(5,5),0)
        frame_threshed = cv2.inRange(frame_blur, color_min_blue, color_max_Blue)
        frame_erode = cv2.erode(frame_threshed ,element,iterations = 3)
        frame_dilate = cv2.dilate(frame_erode,element,iterations = 3)
        frame_dilate2 = cv2.dilate(frame_dilate,element,iterations = 20)
        frame_final = cv2.erode(frame_dilate2,element,iterations = 20)
        frame_vide = cv2.erode(frame_dilate2,element,iterations = 20)
        frame_vide[0:480,0:640] = 0  
        csBlue,_ = cv2.findContours( frame_final, mode=cv2.RETR_LIST,method=cv2.CHAIN_APPROX_SIMPLE )
        _ = np.zeros(frame_final.shape[0:2])
        _ = np.zeros(frame_final.shape[0:2])
        if (csBlue):
            for i in range(len(csBlue)):
                c = csBlue[i-1]
                Perimeter = cv2.arcLength(c,True)
                error = int(Perimeter)/10
                x,y,w,h = cv2.boundingRect(c)
                ymin = y - error
                ymax = y + h + error
                xmin = x - error
                xmax = x + w + error
                if(x-error<=0):
                    xmin = 0
                if(y-error<=0):
                    ymin = 0
                frame_vide[ymin:ymax, xmin:xmax] = 255
                Frame_With_Only_Blue = cv2.bitwise_and(frame,frame, mask = frame_vide)
                Color_MinBrown = np.array([self.H_MINBrown, self.S_MINBrown, self.V_MINBrown],np.uint8)
                Color_MaxBrown = np.array([self.H_MAXBrown, self.S_MAXBrown, self.V_MAXBrown],np.uint8)
                elementBrown = cv2.getStructuringElement(cv2.MORPH_CROSS,(ParamErode,ParamErode))
                Frame_hsvBrown  = cv2.cvtColor(Frame_With_Only_Blue, cv2.COLOR_BGR2HSV)
                Frame_blurBrown = cv2.GaussianBlur(Frame_hsvBrown ,(5,5),0)
                Frame_threshedBrown = cv2.inRange(Frame_blurBrown, Color_MinBrown, Color_MaxBrown)
                Frame_erodeBrown = cv2.erode(Frame_threshedBrown ,elementBrown,iterations = 3)
                Frame_dilateBrown = cv2.dilate(Frame_erodeBrown,elementBrown,iterations = 3)
                Frame_dilate2Brown = cv2.dilate(Frame_dilateBrown,elementBrown,iterations = 20)
                Frame_finalBrown = cv2.erode(Frame_dilate2Brown,elementBrown,iterations = 20)
                Contour_Brown,_ = cv2.findContours( Frame_finalBrown, mode=cv2.RETR_LIST,method=cv2.CHAIN_APPROX_SIMPLE )
                _ = np.zeros(Frame_finalBrown.shape[0:2])
                _ = np.zeros(Frame_finalBrown.shape[0:2])
                BigestPerimeter = 0
                Largest_Contour = 0
                Find_One_Contour = False
                if (Contour_Brown):
                    for i in range(len(Contour_Brown)):
                        Individual_Contour_Brown = Contour_Brown[i - 1]
                        Perimeter = cv2.arcLength(Individual_Contour_Brown,True)
                        if Perimeter > BigestPerimeter:
                            BigestPerimeter = Perimeter
                            Largest_Contour = Individual_Contour_Brown
                            Find_One_Contour = True
                    Individual_Contour_Brown = Largest_Contour    
                    Mass_Of_Brown_Puck = cv2.moments(Individual_Contour_Brown)
                    if (Find_One_Contour):
                        if Mass_Of_Brown_Puck['m00'] != 0:  
                            Center_Of_The_Mass = ( Mass_Of_Brown_Puck['m10']/Mass_Of_Brown_Puck['m00'],Mass_Of_Brown_Puck['m01']/Mass_Of_Brown_Puck['m00'] )
                            (Position_Pixel_x,Position_Pixel_y) = Center_Of_The_Mass
                            return (Position_Pixel_x,Position_Pixel_y)
        #if not found
        return -1,-1
    
    def findOrangePuck(self):
        color_min_orange, color_max_orange = self.getColorArray(3)
        ParamErode = 3
        frame = self.getImage()
        element = cv2.getStructuringElement(cv2.MORPH_CROSS,(ParamErode,ParamErode))
        frame_hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_blur = cv2.GaussianBlur(frame_hsv ,(5,5),0)
        frame_threshed = cv2.inRange(frame_blur, color_min_orange, color_max_orange)
        frame_erode = cv2.erode(frame_threshed ,element,iterations = 3)
        frame_dilate = cv2.dilate(frame_erode,element,iterations = 3)
        frame_dilate2 = cv2.dilate(frame_dilate,element,iterations = 20)
        frame_final = cv2.erode(frame_dilate2,element,iterations = 20)
        frame_vide = cv2.erode(frame_dilate2,element,iterations = 20)
        frame_vide[0:480,0:640] = 0  
        csOrange,_ = cv2.findContours( frame_final, mode=cv2.RETR_LIST,method=cv2.CHAIN_APPROX_SIMPLE )
        _ = np.zeros(frame_final.shape[0:2])
        _ = np.zeros(frame_final.shape[0:2])
        if (csOrange):
            for i in range(len(csOrange)):
                c = csOrange[i-1]
                Perimeter = cv2.arcLength(c,True)
                error = int(Perimeter)/10
                x,y,w,h = cv2.boundingRect(c)
                ymin = y - error
                ymax = y + h + error
                xmin = x - error
                xmax = x + w + error
                if(x-error<=0):
                    xmin = 0
                if(y-error<=0):
                    ymin = 0
                frame_vide[ymin:ymax, xmin:xmax] = 255
                frame_With_Only_Orange = cv2.bitwise_and(frame,frame, mask = frame_vide)
                color_MinWhite , color_MaxWhite = self.getColorArray(9)
                elementWhite = cv2.getStructuringElement(cv2.MORPH_CROSS,(ParamErode,ParamErode))
                frame_hsvWhite  = cv2.cvtColor(frame_With_Only_Orange, cv2.COLOR_BGR2HSV)
                frame_blurWhite = cv2.GaussianBlur(frame_hsvWhite ,(5,5),0)
                frame_threshedWhite = cv2.inRange(frame_blurWhite, color_MinWhite, color_MaxWhite)
                frame_erodeWhite = cv2.erode(frame_threshedWhite ,elementWhite,iterations = 3)
                frame_dilateWhite = cv2.dilate(frame_erodeWhite,elementWhite,iterations = 3)
                frame_dilate2White = cv2.dilate(frame_dilateWhite,elementWhite,iterations = 20)
                frame_finalWhite = cv2.erode(frame_dilate2White,elementWhite,iterations = 20)
                Contour_White,_ = cv2.findContours( frame_finalWhite, mode=cv2.RETR_LIST,method=cv2.CHAIN_APPROX_SIMPLE )
                _ = np.zeros(frame_finalWhite.shape[0:2])
                _ = np.zeros(frame_finalWhite.shape[0:2])
                bigestPerimeter = 0
                largest_Contour = 0
                find_One_Contour = False
                if (Contour_White):
                    for i in range(len(Contour_White)):
                        Individual_Contour_White = Contour_White[i - 1]
                        Perimeter = cv2.arcLength(Individual_Contour_White,True)
                        if Perimeter > bigestPerimeter:
                            bigestPerimeter = Perimeter
                            largest_Contour = Individual_Contour_White
                            find_One_Contour = True
                    Individual_Contour_White = largest_Contour    
                    massOfWhitePuck = cv2.moments(Individual_Contour_White)
                    if (find_One_Contour):
                        if massOfWhitePuck['m00'] != 0:  
                            Center_Of_The_Mass = ( massOfWhitePuck['m10']/massOfWhitePuck['m00'],massOfWhitePuck['m01']/massOfWhitePuck['m00'] )
                            (position_Pixel_x,position_Pixel_y) = Center_Of_The_Mass
                            return (position_Pixel_x,position_Pixel_y)
        #if not found
        return -1,-1   
    
    def findPurplePuck(self):
        color_min_orange, color_max_orange = self.getColorArray(3) 
        imgThreshedOrangeAndPurple = self.thesholdForASpecificColor(color_min_orange, color_max_orange) 
        positionOrangeAndWhiteX, positionOrangeAndWhiteY = self.findOrangePuck()
        if positionOrangeAndWhiteX != -1:
            DiscardSize = 80
            xmin = positionOrangeAndWhiteX - DiscardSize
            ymin = positionOrangeAndWhiteY - DiscardSize
            xmax = positionOrangeAndWhiteX + DiscardSize
            ymax = positionOrangeAndWhiteY + DiscardSize
            if xmin < 0 :
                xmin = 0
            if ymin < 0:
                ymin = 0
            imgThreshedOrangeAndPurple[ymin:ymax,xmin:xmax] = 0
        contour_OrangeAndPurple,_ = cv2.findContours( imgThreshedOrangeAndPurple, mode=cv2.RETR_LIST,method=cv2.CHAIN_APPROX_SIMPLE )
        _ = np.zeros(imgThreshedOrangeAndPurple.shape[0:2])
        _ = np.zeros(imgThreshedOrangeAndPurple.shape[0:2])
        bigestPerimeter = 0
        largest_Contour = 0
        find_One_Contour = False
        if (contour_OrangeAndPurple):
            for i in range(len(contour_OrangeAndPurple)):
                individualContourOrangeAndPurple = contour_OrangeAndPurple[i - 1]
                Perimeter = cv2.arcLength(individualContourOrangeAndPurple,True)
                if Perimeter > bigestPerimeter:
                    bigestPerimeter = Perimeter
                    largest_Contour = individualContourOrangeAndPurple
                    find_One_Contour = True
            individualContourOrangeAndPurple = largest_Contour    
            massOfOrangeAndPurplePuck = cv2.moments(individualContourOrangeAndPurple)
            if (find_One_Contour):
                if massOfOrangeAndPurplePuck['m00'] != 0:  
                    Center_Of_The_Mass = ( massOfOrangeAndPurplePuck['m10']/massOfOrangeAndPurplePuck['m00'],massOfOrangeAndPurplePuck['m01']/massOfOrangeAndPurplePuck['m00'] )
                    (Position_Pixel_x,Position_Pixel_y) = Center_Of_The_Mass
                    return (Position_Pixel_x,Position_Pixel_y)
        #if not found
        return -1,-1 
    
    def findRedPuck(self):
        color_min_red, color_max_red = self.getColorArray(2) 
        imgThreshedRed = self.thesholdForASpecificColor(color_min_red, color_max_red) 
        positionOrangeAndWhiteX, positionOrangeAndWhiteY = self.findOrangePuck()
        if positionOrangeAndWhiteX != -1:
            DiscardSize = 80
            xmin = positionOrangeAndWhiteX - DiscardSize
            ymin = positionOrangeAndWhiteY - DiscardSize
            xmax = positionOrangeAndWhiteX + DiscardSize
            ymax = positionOrangeAndWhiteY + DiscardSize
            if xmin < 0 :
                xmin = 0
            if ymin < 0:
                ymin = 0
            imgThreshedRed[ymin:ymax,xmin:xmax] = 0
        contour_Red,_ = cv2.findContours( imgThreshedRed, mode=cv2.RETR_LIST,method=cv2.CHAIN_APPROX_SIMPLE )
        _ = np.zeros(imgThreshedRed.shape[0:2])
        _ = np.zeros(imgThreshedRed.shape[0:2])
        bigestPerimeter = 0
        largest_Contour = 0
        find_One_Contour = False
        if (contour_Red):
            for i in range(len(contour_Red)):
                individualContourRed = contour_Red[i - 1]
                Perimeter = cv2.arcLength(individualContourRed,True)
                if Perimeter > bigestPerimeter:
                    bigestPerimeter = Perimeter
                    largest_Contour = individualContourRed
                    find_One_Contour = True
            individualContourRed = largest_Contour    
            massOfRedPuck = cv2.moments(individualContourRed)
            if (find_One_Contour):
                if massOfRedPuck['m00'] != 0:  
                    Center_Of_The_Mass = ( massOfRedPuck['m10']/massOfRedPuck['m00'],massOfRedPuck['m01']/massOfRedPuck['m00'] )
                    (Position_Pixel_x,Position_Pixel_y) = Center_Of_The_Mass
                    return (Position_Pixel_x,Position_Pixel_y)
        #if not found
        return -1,-1 
    
    def findWhitePuck(self):
        color_min_cyan = np.array([self.H_MINCyan, self.S_MINCyan, self.V_MINCyan],np.uint8)
        color_max_cyan = np.array([self.H_MAXCyan, self.S_MAXCyan, self.V_MAXCyan],np.uint8)  
        ParamErode = 3
        frame = self.getImage()
        element = cv2.getStructuringElement(cv2.MORPH_CROSS,(ParamErode,ParamErode))
        frame_hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_blur = cv2.GaussianBlur(frame_hsv ,(5,5),0)
        frame_threshed = cv2.inRange(frame_blur, color_min_cyan, color_max_cyan)
        frame_erode = cv2.erode(frame_threshed ,element,iterations = 3)
        frame_dilate = cv2.dilate(frame_erode,element,iterations = 3)
        frame_dilate2 = cv2.dilate(frame_dilate,element,iterations = 20)
        frame_final = cv2.erode(frame_dilate2,element,iterations = 20)
        frame_vide = cv2.erode(frame_dilate2,element,iterations = 20)
        frame_vide[0:480,0:640] = 0  
        csBlue,_ = cv2.findContours( frame_final, mode=cv2.RETR_LIST,method=cv2.CHAIN_APPROX_SIMPLE )
        _ = np.zeros(frame_final.shape[0:2])
        _ = np.zeros(frame_final.shape[0:2])
        if (csBlue):
            for i in range(len(csBlue)):
                c = csBlue[i-1]
                Perimeter = cv2.arcLength(c,True)
                error = int(Perimeter)/10
                x,y,w,h = cv2.boundingRect(c)
                ymin = y - error
                ymax = y + h + error
                xmin = x - error
                xmax = x + w + error
                if(x-error<=0):
                    xmin = 0
                if(y-error<=0):
                    ymin = 0
                frame_vide[ymin:ymax, xmin:xmax] = 255
                Frame_With_Only_Blue = cv2.bitwise_and(frame,frame, mask = frame_vide)
                Color_MinWhite, Color_MaxWhite = self.getColorArray(9)
                elementWhite = cv2.getStructuringElement(cv2.MORPH_CROSS,(ParamErode,ParamErode))
                frame_hsvWhite  = cv2.cvtColor(Frame_With_Only_Blue, cv2.COLOR_BGR2HSV)
                frame_blurWhite = cv2.GaussianBlur(frame_hsvWhite ,(5,5),0)
                frame_threshedWhite = cv2.inRange(frame_blurWhite, Color_MinWhite, Color_MaxWhite)
                frame_erodeWhite = cv2.erode(frame_threshedWhite ,elementWhite,iterations = 3)
                frame_dilateWhite = cv2.dilate(frame_erodeWhite,elementWhite,iterations = 3)
                frame_dilate2White = cv2.dilate(frame_dilateWhite,elementWhite,iterations = 20)
                frame_finalWhite = cv2.erode(frame_dilate2White,elementWhite,iterations = 20)
                contourWhite,_ = cv2.findContours( frame_finalWhite, mode=cv2.RETR_LIST,method=cv2.CHAIN_APPROX_SIMPLE )
                _ = np.zeros(frame_finalWhite.shape[0:2])
                _ = np.zeros(frame_finalWhite.shape[0:2])
                bigestPerimeter = 0
                largest_Contour = 0
                find_One_Contour = False
                if (contourWhite):
                    for i in range(len(contourWhite)):
                        individualContourWhite = contourWhite[i - 1]
                        Perimeter = cv2.arcLength(individualContourWhite,True)
                        if Perimeter > bigestPerimeter:
                            bigestPerimeter = Perimeter
                            largest_Contour = individualContourWhite
                            find_One_Contour = True
                    individualContourWhite = largest_Contour    
                    massOfWhitePuck = cv2.moments(individualContourWhite)
                    if (find_One_Contour):
                        if massOfWhitePuck['m00'] != 0:  
                            centerOfMass = ( massOfWhitePuck['m10']/massOfWhitePuck['m00'],massOfWhitePuck['m01']/massOfWhitePuck['m00'] )
                            (Position_Pixel_x,Position_Pixel_y) = centerOfMass
                            return (Position_Pixel_x,Position_Pixel_y)
        #if not found
        return -1,-1
    
    def findBlackPuck(self):
        Maxpixel = 0
        Xmin = 0
        Xmax = 0
        Ymin = 0
        Ymax = 0
        squareList = list()
        colorMinCyan = np.array([self.H_MINCyan, self.S_MINCyan, self.V_MINCyan],np.uint8)
        colorMaxCyan = np.array([self.H_MAXCyan, self.S_MAXCyan, self.V_MAXCyan],np.uint8)  
        paramErode = 3
        frame = self.getImage()
        element = cv2.getStructuringElement(cv2.MORPH_CROSS,(paramErode,paramErode))
        frame_hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_blur = cv2.GaussianBlur(frame_hsv ,(5,5),0)
        frame_threshed = cv2.inRange(frame_blur, colorMinCyan, colorMaxCyan)
        frame_erode = cv2.erode(frame_threshed ,element,iterations = 3)
        frame_dilate = cv2.dilate(frame_erode,element,iterations = 3)
        frame_dilate2 = cv2.dilate(frame_dilate,element,iterations = 20)
        frame_final = cv2.erode(frame_dilate2,element,iterations = 20)
        frame_vide = cv2.erode(frame_dilate2,element,iterations = 20)
        frame_vide[0:480,0:640] = 0 
        cs,_ = cv2.findContours( frame_final, mode=cv2.RETR_LIST,method=cv2.CHAIN_APPROX_SIMPLE )
        _ = np.zeros(frame_final.shape[0:2])
        _ = np.zeros(frame_final.shape[0:2])
        if (cs):
            for i in range(len(cs)):
                temp = list()
                c = cs[i-1]
                Perimeter = cv2.arcLength(c,True)
                error = int(Perimeter)/10
                x,y,w,h = cv2.boundingRect(c)
                ymin = y - error
                ymax = y + h + error
                xmin = x - error
                xmax = x + w + error
                if(x-error<=0):
                    xmin = 0
                if(y-error<=0):
                    ymin = 0
                if(y+error+h >= 480):
                    ymax = 480
                if(x+w+error>=640):
                    xmax = 640
                temp.append(xmin)
                temp.append(xmax)
                temp.append(ymin)
                temp.append(ymax)
                squareList.append(temp)
                frame_vide[ymin:ymax, xmin:xmax] = 255
            frameWithOnlyCyan = cv2.bitwise_and(frame,frame, mask = frame_vide)
            im_gray = cv2.cvtColor(frameWithOnlyCyan, cv2.COLOR_BGR2GRAY)
            _, im_bw = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            for i in range(0,len(squareList)):
                pixelCounter = 0
                for x in range(squareList[i][0]+1, squareList[i][1]-1):
                    for y in range(squareList[i][2]+1,squareList[i][3]-1):
                        if (im_bw[y,x] == 0):
                            pixelCounter = pixelCounter + 1
                if pixelCounter > Maxpixel and pixelCounter > 1500:
                    Maxpixel = pixelCounter
                    Xmin = squareList[i][0]
                    Xmax = squareList[i][1]
                    Ymin = squareList[i][2]
                    Ymax = squareList[i][3]
            if  Xmin > 0 and Xmax>0 and Ymin > 0 and Ymax >0:
                midllePixelOfBlackSquareX = (Xmax - Xmin)/2 + Xmin
                midllePixelOfBlackSquareY = (Ymax - Ymin)/2 + Ymin
                return midllePixelOfBlackSquareX, midllePixelOfBlackSquareY 
        #if not found
        return -1, -1
        
    def findGrayPuck(self):
        colorMinCyan = np.array([self.H_MINCyan, self.S_MINCyan, self.V_MINCyan],np.uint8)
        colorMaxCyan = np.array([self.H_MAXCyan, self.S_MAXCyan, self.V_MAXCyan],np.uint8)
        imgThreshedCyan = self.thesholdForASpecificColor(colorMinCyan, colorMaxCyan) 
        positionCyanAndBlackX, positionCyanAndBlackY = self.findBlackPuck()
        if positionCyanAndBlackX != -1:
            discardSize = 80
            xmin = positionCyanAndBlackX - discardSize
            ymin = positionCyanAndBlackY - discardSize
            xmax = positionCyanAndBlackX + discardSize
            ymax = positionCyanAndBlackY + discardSize
            if xmin < 0 :
                xmin = 0
            if ymin < 0:
                ymin = 0
            imgThreshedCyan[ymin:ymax,xmin:xmax] = 0
        positionCyanAndWhiteX, positionCyanAndWhiteY = self.findWhitePuck()
        if positionCyanAndWhiteX != -1:
            discardSize = 80
            xmin = positionCyanAndWhiteX - discardSize
            ymin = positionCyanAndWhiteY - discardSize
            xmax = positionCyanAndWhiteX + discardSize
            ymax = positionCyanAndWhiteY + discardSize
            if xmin < 0 :
                xmin = 0
            if ymin < 0:
                ymin = 0
            imgThreshedCyan[ymin:ymax,xmin:xmax] = 0
        contourCyanAndGray,_ = cv2.findContours( imgThreshedCyan, mode=cv2.RETR_LIST,method=cv2.CHAIN_APPROX_SIMPLE )
        _ = np.zeros(imgThreshedCyan.shape[0:2])
        _ = np.zeros(imgThreshedCyan.shape[0:2])
        BigestPerimeter = 0
        Largest_Contour = 0
        Find_One_Contour = False
        if (contourCyanAndGray):
            for i in range(len(contourCyanAndGray)):
                individualContourCyanAndGray = contourCyanAndGray[i - 1]
                Perimeter = cv2.arcLength(individualContourCyanAndGray,True)
                if Perimeter > BigestPerimeter:
                    BigestPerimeter = Perimeter
                    Largest_Contour = individualContourCyanAndGray
                    Find_One_Contour = True
            individualContourCyanAndGray = Largest_Contour    
            massOfCyanAndGrayPuck = cv2.moments(individualContourCyanAndGray)
            if (Find_One_Contour):
                if massOfCyanAndGrayPuck['m00'] != 0:  
                    center_Of_The_Mass = ( massOfCyanAndGrayPuck['m10']/massOfCyanAndGrayPuck['m00'],massOfCyanAndGrayPuck['m01']/massOfCyanAndGrayPuck['m00'] )
                    (Position_Pixel_x,Position_Pixel_y) = center_Of_The_Mass
                    return (Position_Pixel_x,Position_Pixel_y)
        #if not found
        return -1,-1         
    
        
