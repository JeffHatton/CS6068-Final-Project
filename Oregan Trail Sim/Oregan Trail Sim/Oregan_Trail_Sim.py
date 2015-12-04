import Actors.Actor
import Data.DataStore
import Actors.VilagerActor
import Tiles.Tile
import time
from Tkinter import *
from TileControl import *
from threading import *

class Application(Frame):

    def createWidgets(self):
        self.lblWood = Label(self)
        self.lblWood["text"] = "Wood:"
        self.lblWood.grid(row=0, column=0)
        self.lblWoodValue = Label(self)
        self.lblWoodValue["text"] = "0"
        self.lblWoodValue.grid(row=0, column=1)

        self.lblFood = Label(self)
        self.lblFood["text"] = "Food:"
        self.lblFood.grid(row=0, column=2)
        self.lblFoodValue = Label(self)
        self.lblFoodValue["text"] = "0"
        self.lblFoodValue.grid(row=0, column=3)


        self.lblStone = Label(self)
        self.lblStone["text"] = "Stone:"
        self.lblStone.grid(row=0, column=4)
        self.lblStoneValue = Label(self)
        self.lblStoneValue["text"] = "0"
        self.lblStoneValue.grid(row=0, column=5)
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.tileControls = list()

        self.dataStore = Data.DataStore.DataStore(10,10,1)        
        for key, value in self.dataStore.EnvTiles.iteritems():
            (x,y) = self.dataStore.TileIdConverter.Convert1dTo2d(key)
            tileControl = TileControl(value, self)
            tileControl.grid(row=int(y + 1), column=int(x))
            self.tileControls.append(tileControl)    

        self.dataStore.StartSim()
        self.refresh()

    def refresh(self):
        for control in self.tileControls:
            control.refresh()

        self.lblWoodValue["text"] = self.dataStore.Village.Wood
        self.lblFoodValue["text"] = self.dataStore.Village.Food
        self.lblStoneValue["text"] = self.dataStore.Village.Stone
        t = Timer(.1, self.refresh)
        t.start()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()

