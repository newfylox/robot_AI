import cv2
import numpy as np
from math import pi, atan, fabs

class Kinect(object):

    # kinect object constructor
    def __init__(self):
        # table dimension 
        self.A = np.float64([[0.89496632, 0.46109905], [0.42728741, -1.02122205]])
        self.B = np.float64([[-50.96887675], [ 7.41995753]])
        self.iteration=0
        self.kinect =   cv2.VideoCapture(cv2.cv.CV_CAP_OPENNI)
        #kinect initiation
        flags, img = self.kinect.read()#@UnusedVariable
        self.busy = False
        self.awaitingToWork = False
    def isBusy(self):
        return self.busy == True
    
    def setToBusy(self):
        self.busy = True
    
    def setToNotBusy(self):
        self.busy = False
    #grab and return an image
    def getImage(self):
        self.kinect.grab()
        flags_i, img_brg = self.kinect.retrieve(None, cv2.cv.CV_CAP_OPENNI_BGR_IMAGE)#@UnusedVariable
        flags_p, img_depth = self.kinect.retrieve(None, cv2.cv.CV_CAP_OPENNI_POINT_CLOUD_MAP)#@UnusedVariable
        flags_n, img_mask = self.kinect.retrieve(None, cv2.cv.CV_CAP_OPENNI_VALID_DEPTH_MASK)#@UnusedVariable
        img_HSV  = cv2.cvtColor(img_brg, cv2.COLOR_BGR2HSV)  
        return img_HSV, img_depth, img_mask
    
    #return the pixels of a selected color
    def getPixelsCouleur(self, img, couleur=1):
        if couleur == 1:#yellow
            S_MIN = 73
            V_MIN = 72
            S_MAX = 255
            V_MAX = 255
            H_MAX = 99
            H_MIN = 15
        elif couleur == 2:#rose
            S_MIN = 70
            V_MIN = 77
            S_MAX = 255
            V_MAX = 255
            H_MAX = 180
            H_MIN = 138
        elif couleur == 3:#bleu
            S_MIN = 65# check the 
            V_MIN = 71
            S_MAX = 255
            V_MAX = 255
            H_MAX = 134
            H_MIN = 106
        #color treshold
        COULEUR_MIN = np.array([H_MIN, S_MIN, V_MIN],np.uint8)
        COULEUR_MAX = np.array([H_MAX, S_MAX, V_MAX],np.uint8)
        #filter
        kernelC = np.ones((2,2),np.uint8)   
        kernelO = np.ones((4,4),np.uint8)   
        #Frame_blur = cv2.GaussianBlur(imgHSV ,(5,5),0)
        Frame_threshed = cv2.inRange(img, COULEUR_MIN, COULEUR_MAX)
        closing = cv2.morphologyEx(Frame_threshed, cv2.MORPH_CLOSE, kernelC)
        img = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernelO)
        
        #list of white pixels
        img2 = img[0:210,:]
        zero = np.nonzero(img2)
        whitePoints =  np.vstack((zero[0], zero[1])).T
        return whitePoints, img
    
    def getPixelsResistance(self, img):
        S_MIN = 68
        V_MIN = 72
        S_MAX = 215
        V_MAX = 212
        H_MAX = 118
        H_MIN = 108

        #color treshold
        COULEUR_MIN = np.array([H_MIN, S_MIN, V_MIN],np.uint8)
        COULEUR_MAX = np.array([H_MAX, S_MAX, V_MAX],np.uint8)
        #filter
        kernelC = np.ones((3,3),np.uint8)      
        #Frame_blur = cv2.GaussianBlur(imgHSV ,(5,5),0)
        Frame_threshed = cv2.inRange(img, COULEUR_MIN, COULEUR_MAX)
        img1 = cv2.morphologyEx(Frame_threshed, cv2.MORPH_CLOSE, kernelC)
        img = cv2.morphologyEx(img1, cv2.MORPH_OPEN, kernelC)
        
        #liste of white pixels
        img2 = img[0:200,:]
        zero = np.nonzero(img2)
        whitePoints =  np.vstack((zero[0], zero[1])).T
        return whitePoints, img
    
    
    #return the median distance XY of a list of pixels
    def getdistanceXY(self, img, mask, pixels):
        xl = []
        yl = []
        for i in range(len(pixels)/2):
            i = i*2
            x = pixels[i][0]
            y = pixels[i][1]
            #verifie s'ils sont bon
            if mask[x,y] == 255:
                x1 = img[x,y][2]*100
                y1 = img[x,y][0]*100
                #ajuste selon l'angle de la kinect
                point = np.float32([[x1],[y1]])
                T = np.dot(self.A,point)+self.B
                x = T[0]
                y = T[1]
                ydiff = 0.02*x
                y = y-ydiff
                if x<235 and x>0:
                    if y<120 and y>0:
                        xl.append(x)
                        yl.append(y)
        #find medians
        x1 = self.median(xl)
        y1 = self.median(yl)
        if x1==None or y1==None or x1>240 or y1>120 or x1<0 or y1<0:
            return None, None
        return x1, y1
    
    # find rebot angle
    def getAngle(self):
        theta = None
        numberOfIterations = 0
        while theta==None:
            numberOfIterations = numberOfIterations + 1
            #take image
            img, depth, mask = self.getImage()
            #find the 3 markers
            pixels1, img1 = self.getPixelsCouleur(img, 1) #@UnusedVariable
            pixels2, img2 = self.getPixelsCouleur(img, 2) #@UnusedVariable
            pixels3, img3 = self.getPixelsCouleur(img, 3) #@UnusedVariable
            #just yellow marker
            if len(pixels3)<7 and len(pixels2)<7 and len(pixels1)>50:
                theta = 0.46 + pi/2
                break
            #just red marker
            elif len(pixels1)<7 and len(pixels2)<7 and len(pixels3)>50:
                theta = 0.46 + 3*pi/2
                break
            #if we don't see the yellow one      
            elif len(pixels1)<7:
                x3, y3 = self.getdistanceXY(depth, mask, pixels3)
                x2, y2 = self.getdistanceXY(depth, mask, pixels2)
                if x2!=None and y2!=None and x3!=None and y3!=None:
                    #check angle
                    if x2>x3:
                        xT = x2-x3
                        if y2>y3:
                            yT = y2-y3
                            theta = (pi/2-atan(xT/yT))+3*pi/2
                        else:
                            yT = y3-y2 
                            theta = atan(xT/yT)+pi         
                    else:
                        xT = x3-x2
                        if y2>y3:
                            yT = y2-y3
                            theta = atan(xT/yT)
                        else:
                            yT = y3-y2  
                            theta = (pi/2-atan(xT/yT)) + pi/2
                    break
            #if we don't see the red one
            elif len(pixels3)<7:
                x1, y1 = self.getdistanceXY(depth, mask, pixels1)
                x2, y2 = self.getdistanceXY(depth, mask, pixels2)
                if x2!=None and y2!=None and x1!=None and y1!=None:
                    #check angle
                    if x2>x1:
                        xT = x2-x1
                        if y2>y1:
                            yT = y2-y1
                            theta = (pi/2-atan(xT/yT))+pi/2
                        else:
                            yT = y1-y2 
                            theta = atan(xT/yT)         
                    else:
                        xT = x1-x2
                        if y2>y1:
                            yT = y2-y1
                            theta = atan(xT/yT) + pi
                        else:
                            yT = y1-y2 
                            theta = (pi/2-atan(xT/yT)) + 3*pi/2
                    break
            #if we see the 2 opposites markers
            else:
                x1, y1 = self.getdistanceXY(depth, mask, pixels1)
                x3, y3 = self.getdistanceXY(depth, mask, pixels3)
                if x1!=None and y1!=None and x3!=None and y3!=None:
                    #find angle
                    if x3>x1:
                        xT = x3-x1
                        if y3>y1:
                            yT = y3-y1
                            theta = (pi/2-atan(xT/yT))+pi/2
                        else:
                            yT = y1-y3 
                            theta = atan(xT/yT)          
                    else:
                        xT = x1-x3
                        if y3>y1:
                            yT = y3-y1
                            theta = atan(xT/yT) + pi
                        else:
                            yT = y1-y3 
                            theta = (pi/2-atan(xT/yT)) + 3*pi/2
                    break
            if numberOfIterations > 3:
                return None
        #angle in degree
        
        angleEnDegree = np.rad2deg(theta)
        return angleEnDegree
            
    #find robot position
    def getPosition(self):
        x = None
        y = None
        numberOfIterations = 0
        while x==None or y==None:
            numberOfIterations = numberOfIterations + 1
            #take picture
            img, depth, mask = self.getImage()      
            pixels2, img2 = self.getPixelsCouleur(img, 2) #@UnusedVariable
            #if we see the green marker in the middle
            if len(pixels2)>7:
                xT, yT = self.getdistanceXY(depth, mask, pixels2)
                if xT!=None and yT!=None:
                    x = xT+3.5
                    y = yT# +3.5 for the middle of the ball
                    break
            #if we only see the yellow marker
            pixels1, img2 = self.getPixelsCouleur(img, 1) #@UnusedVariable
            pixels3, img2 = self.getPixelsCouleur(img, 3) #@UnusedVariable
            if len(pixels3)<7 and len(pixels2)<7 and len(pixels1)>30:
                xT, yT = self.getdistanceXY(depth, mask, pixels1)
                if xT!=None and yT!=None:
                    x = xT+19
                    y = yT+8
                    break
            #if we only see the red marker
            elif len(pixels1)<7 and len(pixels2)<7 and len(pixels3)>30:
                xT, yT = self.getdistanceXY(depth, mask, pixels3)
                if xT!=None and yT!=None:
                    x = xT+19
                    y = yT+8
                    break
            #with hte two opposites markers  
            else:
                x1, y1 = self.getdistanceXY(depth, mask, pixels1)
                x2, y2 = self.getdistanceXY(depth, mask, pixels3)
                if x1!=None and y1!=None and x2!=None and y2!=None:
                #cfind position
                    if x1>x2:
                        xT = (x1-x2)/2
                        x = x2+xT
                        if y1>y2:
                            yT = (y1-y2)/2
                            y = y2+yT
                        else:
                            yT = (y2-y1)/2
                            y = y1+yT            
                    else:
                        xT = (x2-x1)/2
                        x = x1+xT
                        if y1>y2:
                            yT = (y1-y2)/2
                            y = y2+yT
                        else:
                            yT = (y2-y1)/2
                            y = y1+yT
                            break
            if numberOfIterations>3:
                return None,None                    
        return x, y
    
    # to check near the resistance
    def getPositionResistance(self):
        x = None
        y = None
        self.iteration = 0 
        while x==None or y==None:
            self.iteration = self.iteration+1
            #get image
            img, depth, mask = self.getImage()      
            pixels, img2 = self.getPixelsResistance(img) #@UnusedVariable
            if len(pixels)>7:
                xT, yT = self.getdistanceXY(depth, mask, pixels)
                if xT!=None and yT!=None:
                    x = xT+11.5
                    y = yT+4
            if self.iteration>3:
                break
        self.iteration = 0                    
        return x, y
    
    #find the towers position
    def getTower(self):
        p1 = None
        p2 = None
        iteration = 0
        while p1 == None or p2 == None:
            iteration = iteration + 1  
            if iteration > 4:
                return None
            img, depth, mask = self.getImage() #@UnusedVariable
            #find the pixels of the two towers
            list1, img = self.getPixelsTowers(img,1)
            if len(list1)<=0:
                return None
            #get their distance
            p1, p2 = self.getdistanceXYTowers(depth, mask, list1, iteration)
            if p1 != None and p2 != None:
                obstaclePositionList = []
                obstaclePositionList.append(p1[0][0])
                obstaclePositionList.append(p1[1][0])
                obstaclePositionList.append(p2[0][0])
                obstaclePositionList.append(p2[1][0])
                return obstaclePositionList
        
        
    def getPixelsTowers(self, img, iteration):
        S_MIN = 215# check the red
        V_MIN = 96
        S_MAX = 255
        V_MAX = 214
        H_MAX = 188
        H_MIN = 162
        #creer les limite du treshhold selon la couleur
        COULEUR_MIN = np.array([H_MIN, S_MIN, V_MIN],np.uint8)
        COULEUR_MAX = np.array([H_MAX, S_MAX, V_MAX],np.uint8)
        #filter and treshold
        kernelC = np.ones((3,3),np.uint8)      
        #Frame_blur = cv2.GaussianBlur(imgHSV ,(5,5),0)
        Frame_threshed = cv2.inRange(img, COULEUR_MIN, COULEUR_MAX)
        img1 = cv2.morphologyEx(Frame_threshed, cv2.MORPH_CLOSE, kernelC)
        img = cv2.morphologyEx(img1, cv2.MORPH_OPEN, kernelC)
                   
        #find pixel of red
        listpixels = []
        height, width = img.shape # @UnusedVariable
        for y in range(390):
            y = y+250
            for x in range(101):
                x=x+140
                if img[x][y] == 255:
                    listpixels.append((x,y))
        
        return listpixels, img
    
    def getdistanceXYTowers(self, img, mask, pixels, iteration):
        points = []
        for i in range(len(pixels)):
            x = pixels[i][0]
            y = pixels[i][1]
            #verifie s'ils sont bon
            if mask[x,y] == 255:
                x1 = img[x,y][2]*100
                y1 = img[x,y][0]*100
                #ajuste selon l'angle de la kinect
                point = np.float32([[x1],[y1]])
                T = np.dot(self.A,point)+self.B
                x = T[0]
                y = T[1]
                ydiff = 0.02*x
                y = y-ydiff
                if x<235 and x>0:
                    if y<120 and y>0:
                        p1 = (x,y)
                        points.append(p1)
        
        if len(points) == 0:
            return None, None         
        list1 = []
        list2 = []
        list1.append(points[0])  
        sumx = 0
        sumy = 0    
        for i in range(len(points)):
            sumx = sumx+points[0][0]
            sumy = sumy+points[0][1]  
            moyx = float(sumx)/len(list1)
            moyy = float(sumy)/len(list1)
            xdiff = points[i][0]-moyx
            ydiff = points[i][1]-moyy
            if iteration==1:
                if fabs(xdiff)>15 or fabs(ydiff)>15:
                    list2.append(points[i])
                else:
                    list1.append(points[i])
            if iteration==2:
                if fabs(xdiff)>20 or fabs(ydiff)>20:
                    list2.append(points[i])
                else:
                    list1.append(points[i])
            if iteration==3:
                if fabs(xdiff)>25 or fabs(ydiff)>25:
                    list2.append(points[i])
                else:
                    list1.append(points[i])
            if iteration==4:
                if fabs(xdiff)>28 or fabs(ydiff)>28:
                    list2.append(points[i])
                else:
                    list1.append(points[i])
        #find medians
        xl1 = [x[0] for x in list1]
        yl1 = [x[1] for x in list1]
        xl2 = [x[0] for x in list2]
        yl2 = [x[1] for x in list2]
        x1 = self.median(xl1) + 6.5
        y1 = self.median(yl1)
        x2 = self.median(xl2) + 6.5
        y2 = self.median(yl2)
        if x1==None or y1==None or x1>240 or y1>120 or x1<0 or y1<0 or x2==None or y2==None or x2>240 or y2>120 or x2<0 or y2<0:
            return None, None
        return (x1,y1), (x2,y2)
        
        
    #median fonction
    def median(self, mylist):
        if len(mylist)==0:
            return None
        sorts = sorted(mylist)
        length = len(sorts)
        if not length % 2:
            return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
        return sorts[length / 2]
    
    #fonction to show an image
    def show(self, img):
        while(1):
            cv2.imshow('Affichage', img)  
            cc = cv2.waitKey(10)
            if cc != -1: # Touche Echap quitte
                break
