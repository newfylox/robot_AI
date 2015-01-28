import serial
import time

#microDue class to control the micro-processor
class MicroDue(object):
    
    def __init__(self):
        self.sc = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__Arduino_Due_Prog._Port_85235353037351703122-if00', 9600, timeout=10)
        time.sleep(0.1)
        self.message = ""
        self.sc.flush()
        
    def closeMicroDue(self):
        self.sc.close()     
        
    def setLedOn(self):
        self.sc.write("A\n")
        self.waitForAck()
        
    def setLedOff(self):
        self.sc.write("B\n")
        self.waitForAck()
    
    def setElectroOn(self):
        self.sc.write("C\n")
        self.waitForAck()
        time.sleep(1)
        
    def setElectroOff(self):
        self.sc.write("D\n")
        self.waitForAck()
        
    def writeLCD(self, message):
        self.sc.write("E-" + message + "\n")
        self.waitForAck()
    
    def moveForward(self, distance):
        time.sleep(0.1)
        dist = str(distance)
        self.sc.write("F-" + dist + "\n")
        self.waitForAck()
        
    def moveBackward(self, distance):
        time.sleep(0.1)
        dist = str(distance)
        self.sc.write("G-" + dist + "\n")
        self.waitForAck()
        
    def moveLeft(self, distance):
        time.sleep(0.1)
        dist = str(distance)
        self.sc.write("H-" + dist + "\n")
        self.waitForAck()
        
    def moveRight(self, distance):
        time.sleep(0.1)
        dist = str(distance)
        self.sc.write("I-" + dist + "\n")
        self.waitForAck()
        
    def rotateClockwise(self, angle):
        time.sleep(0.1)
        dist = str(angle)
        self.sc.write("J-" + dist + "\n")
        self.waitForAck()
    
    def rotateCounterClockwise(self, angle):
        time.sleep(0.1)
        dist = str(angle)   
        self.sc.write("K-" + dist + "\n")
        self.waitForAck()
        
    def readResistance(self):
        time.sleep(0.1)
        self.sc.write("L\n")
        res = 0
        while True:
            try:
                res = self.sc.readline()
                if "ok" in res:
                    res = res.replace("ok\n", "")
                    res = float(res)
                    res = round(res*0.97,2)
                    res = str(res)
                    return res
            except:
                pass
            break

    def hasPuck(self):
        while not self.sc.isOpen():
            time.sleep(0.1)
        self.sc.write("M\n")
        while True:
            try:
                value = self.sc.readline()
                time.sleep(0.01)
                return value
            except:
                pass
            break
        self.waitForAck() 
                
    def waitForAck(self):
        while True:
            try:
                time.sleep(0.01)
                state = self.sc.readline()
                if "ok" in state:
                    return True
            except:
                pass
            break
