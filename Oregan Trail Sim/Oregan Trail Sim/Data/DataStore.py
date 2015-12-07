﻿import Ids.IdConverter
import threading
import Villlages.Village
import Villlages.Buildings
import Villlages.Buildings.StockPile
import xml.etree.ElementTree as ET

from Tiles.TileGenerator import *
from Actors.VilagerActor import *
from Logger.Logger import *
from Actors.NeedAnalyzer import *

class DataStore(object):
    """Global Storage for Application"""

    def __init__(self, initFile): #x, y, numVillagers):
        tree = ET.parse('init.xml')
        root = tree.getroot()
        x = int(root.attrib.get("width"))
        y = int(root.attrib.get("height"))
        seed = root.find("TileGenerator").text

        self.EnvActors = dict()
        self.EnvTiles = dict()
        self.SetEnvironmentDim(x, y)
        self.ActorLock = threading.Lock()
        self.EnvLock = threading.Lock()
        self.Village = Villlages.Village.Village(self)              
        self.MiscLock = threading.Lock()
        self.Logger = Logger(3)
        self.OtherActors = dict()
        self.HousingAvilable = 0 
        self.ProspectiveHousing = 0
        for tile in TileGenerator.generateTileGrid(x, y, seed):
            tile.ID.LocalId = self.TileIdConverter.Convert2dTo1d(tile.ID.IdX,tile.ID.IdY)
            self.AddTile(tile)

        numVillagers = int(root.attrib.get("villagers"))
        for idx in range(numVillagers):
            actor = VilagerActor(self, self.EnvTiles[x /2 + y/2])
            self.AddActor(actor)

        while True:
            id = random.randint(0, (x * y) -1)
            if self.EnvTiles[id].ResourceType == "None":
                self.EnvTiles[id].Structure = Villlages.Buildings.StockPile.StockPile(self, self.EnvTiles[id])
                self.Village.addNeeds([VillageRequest("Build:{0}".format(id), 0)])
                self.Village.addNeeds([VillageRequest("Build:{0}".format(id), 0)])
                break
        needActor = NeedAnalyzer(self)
        self.OtherActors[needActor.ID.GUID] = needActor
        needActor.start()

    def addHousing(self, amount):
        self.MiscLock.acquire()
        self.HousingAvilable += amount
        self.MiscLock.release()

    def addProspective(self, amount):
        self.MiscLock.acquire()
        self.ProspectiveHousing += amount
        self.MiscLock.release()

    def AddActor(self, actor):
        self.ActorLock.acquire()
        self.EnvActors[actor.ID.GUID] = actor
        self.ActorLock.release()

    def RemoveActor(self, id):
        actor = self.EnvActors.get(id, None)
        if actore != None:
            del self.EnvActors[id]
            actor.stop_requested = True
    
    def MorpthActor(self, id, newActorType):
        print("Implement morpth actor")

    def AddTile(self, tile):
        self.EnvLock.acquire()
        self.EnvTiles[tile.ID.LocalId] = tile
        self.EnvLock.release()

    def RemoveTile(self, id):
        print("Implement remove Tile")
    
    def MorpthTile(self, id, newTileType):
        print("Implement morpth Tile")

    def SetEnvironmentDim(self, x, y):
        self.TileIdConverter = Ids.IdConverter.IdConverter(x, y, False)
        self.EnvironmentDimX = x
        self.EnvironmentDimY = y

    def StartSim(self):
        for key,actor in self.EnvActors.iteritems():
            actor.start()

    def AllResources(self):
        return ["Wood", "Food", "Stone", "Iron"]

    def EndSim(self):
        for key,actor in self.EnvActors.iteritems():
            actor.stop_requested = True
        for key,actor in self.OtherActors.iteritems():
            actor.stop_requested = True
        self.Logger.saveToFile()