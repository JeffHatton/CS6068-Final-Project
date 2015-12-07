import Actors.Actor
import Data.DataStore
import Actors.VilagerActor
import Tiles.Tile
import time
from Tkinter import *
from TileControl import *
from threading import *
from EnvironmentControl import *

class Application(Frame):

    def createWidgets(self):
        self.lblTimeScaling = Label(self)
        self.lblTimeScaling["text"] = "Time Scaling:"     
        self.lblTimeScaling.grid(row=0, column=0,columnspan = 1)
        self.entrTimeScaling = Entry(self, textvariable=self.dataStore.TimeScaling)
        self.entrTimeScaling.grid(row=0, column=1,columnspan = 1)
        self.EnvControl = EnvironmentControl(self)
        self.EnvControl.grid(row=1, column=0)
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.tileControls = list()
        self.alive = True

        self.dataStore = Data.DataStore.DataStore('init.xml')#width,height,villagers)        
        
        self.createWidgets()

        self.dataStore.StartSim()
        self.EnvControl.refresh()

    def onClose(self):
        self.dataStore.EndSim()
        self.alive = False
        time.sleep(0.2)
        self.master.destroy()

root = Tk()
app = Application(master=root)
root.protocol("WM_DELETE_WINDOW", app.onClose)
app.mainloop()

