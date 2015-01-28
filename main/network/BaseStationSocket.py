import socket
import time
from main.constants import PORT_NUMBER


class BaseStationSocket(object):
    
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def startConnection(self, ipServerAddress):
        serverInformations = (ipServerAddress, PORT_NUMBER)
        self.sock.connect(serverInformations)
    
    def stopConnection(self):
        self.sock.close()
            
    def sendDataToRobot(self, data):
        data = str(data)
        self.sock.sendall(data)
        time.sleep(0.1)
        
    def receiveDataFromRobot(self):
        data = self.sock.recv(4096)
        data = str(data)
        return data