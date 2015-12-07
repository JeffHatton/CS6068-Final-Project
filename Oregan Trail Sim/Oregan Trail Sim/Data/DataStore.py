import Ids.IdConverter
import threading
import Villlages.Village
import Villlages.Buildings
import Villlages.Buildings.StockPile
import xml.etree.ElementTree as ET
import math
from Tiles.TileGenerator import *
from Actors.VilagerActor import *
from Logger.Logger import *
from Actors.NeedAnalyzer import *

class DataStore(object):
    """Global Storage for Application"""

    def __init__(self, initFile): #x, y, numVillagers):
        tree = ET.parse('init.xml')
        root = tree.getroot()
        self.x = int(root.attrib.get("width"))
        self.y = int(root.attrib.get("height"))
        x = self.x
        y = self.y
        seed = root.find("TileGenerator").text

        self.EnvActors = dict()
        self.EnvTiles = dict()
        self.SetEnvironmentDim(x, y)
        self.ActorLock = threading.Lock()
        self.EnvLock = threading.Lock()
        self.Village = Villlages.Village.Village(self)              
        self.VillageCenter = (x * y) / 50
        self.MiscLock = threading.Lock()
        self.Logger = Logger(0)
        self.OtherActors = dict()
        self.HousingAvilable = 0 
        self.NumBuildings = 0
        self.ProspectiveHousing = 0
        self.refineMap = {"Food" : "FoodProcessor", "PIron": "IronProcessor" , "PStone":"StoneProcessor"}
        for tile in TileGenerator.generateTileGrid(x, y, seed):
            tile.ID.LocalId = self.TileIdConverter.Convert2dTo1d(tile.ID.IdX,tile.ID.IdY)
            self.AddTile(tile)

        while True:
            id = random.randint(0, (x * y) -1)
            if self.EnvTiles[id].Walkable:
                numVillagers = int(root.attrib.get("villagers"))
                for idx in range(numVillagers):
                    actor = VilagerActor(self, self.EnvTiles[x /2 + y/2])
                    self.AddActor(actor)
                break       

        #while True:
        #    id = random.randint(0, (x * y) -1)
        #    if self.EnvTiles[id].ResourceType == "None":
        #        self.EnvTiles[id].Structure = Villlages.Buildings.StockPile.StockPile(self, self.EnvTiles[id])
        #        self.Village.addNeed(VillageRequest("Build:{0}".format(id), 0), 2)
        #        break
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
        if actor != None:
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
        return ["Wood", "Food", "Stone", "Iron", "PIron", "PStone"]

    def gatherableResources(self):
        return ["Wood", "Food", "Stone", "Iron"]

    def rawResources(self):
        return ["Stone", "Iron"]

    def processedResources(self):
        return ["PStone", "PIron"]

    def EndSim(self):
        for key,actor in self.EnvActors.iteritems():
            actor.stop_requested = True
        for key,actor in self.OtherActors.iteritems():
            actor.stop_requested = True
        self.Logger.saveToFile()

    def AddBuilding(self, amount):
        self.MiscLock.acquire()
        self.NumBuildings += amount
        self.MiscLock.release()


    def searchTiles(self, searchValue, searchFunction):
        tileId = -1

        for searchDistance in range(0,self.x):
            for x in range(-searchDistance, searchDistance):
                id = self.TileIdConverter.Convert2dTo1d(self.x / 2 + x, self.y / 2 + searchDistance)
                if id >= 0:                    
                    if  searchFunction(self.EnvTiles[id], searchValue):
                        return id
                id = self.TileIdConverter.Convert2dTo1d(self.x / 2 + x, self.y / 2 -searchDistance)
                if id >= 0:
                    if searchFunction(self.EnvTiles[id], searchValue):
                        return id
            for y in range(-searchDistance, searchDistance):
                id = self.TileIdConverter.Convert2dTo1d(self.x / 2 + searchDistance, self.y / 2 + y)
                if id >= 0:
                    if searchFunction(self.EnvTiles[id], searchValue):
                        return id
                id = self.TileIdConverter.Convert2dTo1d(self.x / 2 -searchDistance, self.y / 2 + y)
                if id >= 0:                   
                    if searchFunction(self.EnvTiles[id], searchValue):
                        return id
        return tileId

    def findIdleBuilding(self, tile, buildingType):
        if tile.Structure != None:
            if tile.Structure.BuildingType == buildingType and not tile.Structure.WorkInProgress:
                return True
        return False

    def findIdle(self, buildingType):
        return self.searchTiles(buildingType, self.findIdleBuilding)

    def isBuildingIdleandBuilt(self, tile, buildingType):
        return tile.Structure.BuildingType == buildingType and tile.Structure.Built and not tile.Structure.WorkInProgress

    def DoesBuildingExist(self, tile, buildingType):
        return tile.Structure.BuildingType == buildingType

    def findAllIdleReadBuildings(self,buildingType, condition):
        ids = list()
        for id, tile in self.EnvTiles.iteritems():
            if tile.Structure != None:
                if condition(tile, buildingType):
                    ids.append(tile.ID.LocalId)
        return ids


    def getBuildingPoint(self):
        count = 0
        if self.NumBuildings == 0 :
            range = 4
        else:
            range = int( max(4, math.log(self.NumBuildings, 2)))
        while True:
            if count > range * range:
                range += 1
            
            x = random.randint(0, range)
            y = random.randint(0, range)
            (curX, curY) = self.TileIdConverter.Convert1dTo2d(self.VillageCenter)
            id = self.TileIdConverter.Convert2dTo1d(curX + x, curY + y)
            if id >= 0:
                if self.EnvTiles[id].ResourceType == "None" and self.EnvTiles[id].Structure == None:
                    return id
                count +=1