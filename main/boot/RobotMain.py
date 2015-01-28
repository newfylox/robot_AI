import Queue
import threading
from main.model.Game import Game
from main.model.Robot import Robot
from main.network.ThreadedClientRobot import ThreadedClientRobot
import sys

def main():
    queue = Queue.Queue()
    robot = Robot(queue)
    game = Game(robot, queue)
    client = ThreadedClientRobot(queue, game)
    
    robotConnectionThread = threading.Thread(target = client.run)
    robotConnectionThread.daemon = True
    robotConnectionThread.start()
    
    #Main running the actions of the game
    while True: 
        if game.isInProcess():             
            game.doAction()
        elif game.isKilled == True:
            sys.exit(0)
       
if __name__ == "__main__":
    main()        


