import serial
import time

class Pololu(object):
    
    def __init__(self):
        self.sc = serial.Serial('/dev/serial/by-id/usb-Pololu_Corporation_Pololu_Micro_Maestro_6-Servo_Controller_00046502-if00')

    def setElectroDown(self):
        self.setAngle(3, 180)
        
    def setElectroUp(self):
        self.setAngle(3, 0)
        
    def setCamUp(self):
        self.setAngle(5, 46)
        time.sleep(1)

    def setCamDown(self):
        self.setAngle(5, 0)
        time.sleep(1)

    def setCamRight(self):
        self.setAngle(4, 180)
        time.sleep(1)
        
    def setCamLeft(self):
        self.setAngle(4, 0)
        time.sleep(1)
        
    def setCamMiddle(self):
        self.setAngle(4, 90)
        time.sleep(1)
    
    def closeServo(self):
        self.sc.close()
        
    def setAngle(self, n, angle):
        if angle > 180 or angle <0:
            angle=90
        byteone=int(254*angle/180)
        bud=chr(0xFF)+chr(n)+chr(byteone)
        self.sc.write(bud)

    def getErrors(self):
        data =  chr(0xaa) + chr(0x0c) + chr(0x21)
        self.sc.write(data)
        w1 = ord(self.sc.read())
        w2 = ord(self.sc.read())
        return w1, w2
        
        
