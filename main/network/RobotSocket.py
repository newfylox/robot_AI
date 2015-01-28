import socket
import sys
import time
import netifaces as ni
from main.constants import PORT_NUMBER

class RobotSocket(object):
    
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client = None

    def startConnection(self, ipServerAddress = None):
        if ipServerAddress:
            serverInformations = (ipServerAddress, PORT_NUMBER)
        else:
            ipServerAddress = ni.ifaddresses(str(sys.argv[1]))[2][0]['addr']
            serverInformations = (ipServerAddress, PORT_NUMBER)
        self.sock.bind(serverInformations)
        self.sock.listen(1)
                
    def stopConnection(self):
        self.sock.close()
        
    def sendDataToBaseStation(self, data):
        if not self.client:
            self.client, _ = self.sock.accept()
        data = str(data)
        self.client.sendall(data)
        time.sleep(1)
        
    def receiveDataFromBaseStation(self):
        if not self.client:
            self.client, _ = self.sock.accept()
        data = self.client.recv(4096)
        data = str(data)
        return data
        
