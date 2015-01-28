import Tkinter
from main.network.ThreadedClientBaseStation import ThreadedClientBaseStation

def main():
    root = Tkinter.Tk()
    client = ThreadedClientBaseStation(root)
    root.after(1000, client.gui.ourBaseStationInterface.updateLabels())
    
    #Main running the GUI
    root.mainloop()

if __name__ == "__main__":
    main()  


    