﻿import Actors.Actor
import Data.DataStore
import Actors.VilagerActor
import Tiles.Tile
import time
from Tkinter import *
from TileControl import *
from threading import *

class EnvironmentControl(Frame):

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

    def __init__(self, dataStore, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.tileControls = list()
        self.alive = True
        self.dataStore = dataStore

        #tree = ET.parse('init.xml')
        #root = tree.getroot()
        #width = int(root.attrib.get("width"))
        #height = int(root.attrib.get("height"))
        #villagers = int(root.attrib.get("villagers"))
        self.dataStore = master.dataStore
        for key, value in self.dataStore.EnvTiles.iteritems():
            (x,y) = self.dataStore.TileIdConverter.Convert1dTo2d(key)
            tileControl = TileControl(value, self)
            #buildingControl = BuildingControl(value.Structure, self)
            tileControl.grid(row=int(y + 2), column=int(x))
            self.tileControls.append(tileControl)

    def refresh(self):
        if not self.alive:
            return

        list = self.dataStore.getAndClearRefresh()

        while len(list) > 0:
            self.tileControls[list.pop().ID.LocalId].refresh()


        #for control in self.tileControls:
        #    control.refresh()

        self.lblWoodValue["text"] = self.dataStore.Village.Resources["Wood"]
        self.lblFoodValue["text"] = self.dataStore.Village.Resources["Food"]
        self.lblStoneValue["text"] = self.dataStore.Village.Resources["Stone"]
        self.lblIronValue["text"] = self.dataStore.Village.Resources["Iron"]
        self.lblLivingValue["text"] = len(self.dataStore.EnvActors)
        #t = Timer(.1, self.refresh)
        #t.start()
        self.master.after(200, self.refresh)
