import Actors.Actor
import Data.DataStore
import Actors.VilagerActor
from Tiles import *
import time
from Tkinter import *

class TileControl(Frame):
    """description of class"""

    def createWidgets(self):
        #self.lblType = Label(self)
        #self.lblType.pack({"side": "top"})

        self.lblCount = Label(self)
        self.lblCount.pack({"side": "left"})       
        self.buildingControl = BuildingControl(self.Tile.Structure, self)
        self.buildingControl.pack({"side": "left"})       

    def __init__(self, tile, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.Tile = tile
        self.createWidgets()        
        self.refresh()

    def refresh(self):
        self.lblCount["text"] = self.Tile.GetActorCount()      
        self.lblCount["background"] = self.typeToColor(self.Tile.ResourceType)
        self.buildingControl.refresh()

    def typeToColor(self, type):
        if type == "Wood":
            return "Green"
        elif type == "Food":
            return "Red"
        elif type == "Stone":
            return "Gray"
        elif type == "Water":
            return "Blue"
        elif type == "Iron":
            return "Pink"
        else:
            return "White"


class BuildingControl(Frame):
    """description of class"""

    def createWidgets(self):
        #self.lblType = Label(self)
        #self.lblType.pack({"side": "top"})

        self.lblCount = Label(self)
        self.lblCount["background"] = "Black"
        self.lblCount.pack({"side": "top"})       

    def __init__(self, Building, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.Building = Building
        self.createWidgets()        
        self.refresh()

    def refresh(self):
        if self.Building == None:
            return

        if self.Building.PercentBuilt != 100:
            self.lblCount["text"] = self.Building.PercentBuilt
            self.lblCount["background"] = "Yellow"
        else:
            self.lblCount["text"] = ""
            self.lblCount["background"] = self.typeToColor(self.Building.BuildingType)

    def typeToColor(self, type):
        if type == "StockPile":
            return "Brown"
        else:
            return "White"

