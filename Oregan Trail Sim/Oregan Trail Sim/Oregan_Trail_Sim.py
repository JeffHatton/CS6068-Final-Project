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

        self.lblIron = Label(self)
        self.lblIron["text"] = "Iron:"
        self.lblIron.grid(row=0, column=6)
        self.lblIronValue = Label(self)
        self.lblIronValue["text"] = "0"
        self.lblIronValue.grid(row=0, column=7)

        self.lblLiving = Label(self)
        self.lblLiving["text"] = "Living:"
        self.lblLiving.grid(row=0, column=8)
        self.lblLivingValue = Label(self)
        self.lblLivingValue["text"] = "0"
        self.lblLivingValue.grid(row=0, column=9)
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.tileControls = list()
        self.alive = True

        #tree = ET.parse('init.xml')
        #root = tree.getroot()
        #width = int(root.attrib.get("width"))
        #height = int(root.attrib.get("height"))
        #villagers = int(root.attrib.get("villagers"))

        self.dataStore = Data.DataStore.DataStore('init.xml')#width,height,villagers)        
        for key, value in self.dataStore.EnvTiles.iteritems():
            (x,y) = self.dataStore.TileIdConverter.Convert1dTo2d(key)
            tileControl = TileControl(value, self)
            #buildingControl = BuildingControl(value.Structure, self)
            tileControl.grid(row=int(y + 1), column=int(x))
            self.tileControls.append(tileControl)    

        self.dataStore.StartSim()
        self.refresh()

    def refresh(self):
        if not self.alive:
            return
        for control in self.tileControls:
            control.refresh()

        self.lblWoodValue["text"] = self.dataStore.Village.Resources["Wood"]
        self.lblFoodValue["text"] = self.dataStore.Village.Resources["Food"]
        self.lblStoneValue["text"] = self.dataStore.Village.Resources["Stone"]
        self.lblIronValue["text"] = self.dataStore.Village.Resources["Iron"]
        self.lblLivingValue["text"] = len(self.dataStore.EnvActors)
        t = Timer(.1, self.refresh)
        t.start()

    def onClose(self):
        self.dataStore.EndSim()
        self.alive = False
        time.sleep(0.2)
        self.master.destroy()

root = Tk()
app = Application(master=root)
root.protocol("WM_DELETE_WINDOW", app.onClose)
app.mainloop()

