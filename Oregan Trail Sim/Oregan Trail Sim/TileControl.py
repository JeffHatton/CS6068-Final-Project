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
        self.lblCount.pack({"side": "top"})

    def __init__(self, tile, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.Tile = tile
        self.refresh()

    def refresh(self):
        self.lblCount["text"] = self.Tile.GetActorCount()      
        self.lblCount["background"] = self.typeToColor(self.Tile.ResourceType)

    def typeToColor(self, type):
        if type == "Wood":
            return "Green"
        elif type == "Food":
            return "Red"
        elif type == "Stone":
            return "Gray"
        elif type == "Water":
            return "Blue"
        else:
            return "White"


