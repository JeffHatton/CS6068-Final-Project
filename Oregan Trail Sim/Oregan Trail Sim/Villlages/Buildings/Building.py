from Data.DataStore import *
from threading import *
import time


class Building(object):
    """description of class"""
    def __init__(self, dataStore, tile):
        self.DataStore = dataStore
        self.ResouceCost = dict()
        for resource in dataStore.AllResources():
            self.ResouceCost[resource] = 0
        self.Wokers = dict()
        self.WokersRequiredToBuild = 0
        self.TimeToBuild = 0
        self.PercentBuilt =0
        self.Tile = tile
        self.BuildingType = ""
        self.Lock = threading.Lock()

    def AddActor(self, actor):
        self.Lock.acquire()
        self.Wokers[actor.ID.GUID] = actor        

        if len(self.Wokers) == self.WokersRequiredToBuild:
            self.DataStore.Village.requestResources(self.ResouceCost)
            self.LastTime = time.time()
            self.Build()
        self.Lock.release()

    def RemoveActor(self, actor):
        self.Lock.acquire()
        #print(self.ActorsInTile)
        #print(self.ID.LocalId)
        del self.Wokers[actor.ID.GUID]
        self.Lock.release()

    def Build(self):
        timenow = time.time()
        diff = timenow - self.LastTime
        self.LastTime = timenow

        self.PercentBuilt += diff / self.TimeToBuild * 100

        if self.PercentBuilt >= 100:
            self.PercentBuilt = 100
            for actor in self.Wokers.values():
                self.RemoveActor(actor)

            return
        t = Timer(.5, self.Build)
        t.start()




