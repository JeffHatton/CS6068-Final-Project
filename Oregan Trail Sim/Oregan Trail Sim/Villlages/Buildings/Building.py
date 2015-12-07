from Data.DataStore import *
from threading import *
import time


class Building(object):
    """description of class"""
    def __init__(self, dataStore, tile):
        self.DataStore = dataStore
        self.ResouceCost = dict()
        self.WorkResourceCost = dict()
        self.WorkResourceProduce = dict()
        for resource in dataStore.AllResources():
            self.ResouceCost[resource] = 0
        for resource in dataStore.AllResources():
            self.WorkResourceCost[resource] = 0
        for resource in dataStore.AllResources():
            self.WorkResourceProduce[resource] = 0
        self.Wokers = dict()
        self.WokersRequiredToBuild = 0
        self.TimeToBuild = 0
        self.PercentBuilt =0
        self.Tile = tile
        self.BuildingType = ""
        self.VillagersRequiredToWork = 0
        self.WorkTime = 0
        self.PercentWorked = 0
        self.Lock = threading.Lock()
        self.WorkFin = False
        self.Built = False
        self.WorkInProgress = False

    def AddActor(self, actor):
        self.Lock.acquire()
        self.Wokers[actor.ID.GUID] = actor        

        self.DataStore.Logger.addToLog("Actor {0} added to Building {1}, length {2} Tile-{3}".format(actor.ID.GUID, self.BuildingType, len(self.Wokers), self.Tile.ID.LocalId), 0)
        self.LastTime = time.time()
        if len(self.Wokers) == self.WokersRequiredToBuild and not self.Built:
            self.Lock.release()            
            self.waitForResources()            
            return 
        elif len(self.Wokers) == self.VillagersRequiredToWork:
            self.Lock.release()
            self.waitForResources()            
            return 
        self.Lock.release()

    def RemoveActor(self, actor):
        self.Lock.acquire()
        del self.Wokers[actor.ID.GUID]
        self.DataStore.Logger.addToLog("Actor {0} removed to Building {1}, length {2}".format(actor.ID.GUID, self.BuildingType, len(self.Wokers)), 0)
        self.Lock.release()

    def Build(self):
        timenow = time.time()
        diff = timenow - self.LastTime
        self.LastTime = timenow

        self.PercentBuilt += diff / self.TimeToBuild * 100

        if self.PercentBuilt >= 100:
            self.PercentBuilt = 100
            self.Built = True
            self.BuildingFinished()
            for actor in self.Wokers.values():
                self.RemoveActor(actor)

            return
        t = Timer(.5  / (float(self.DataStore.TimeScaling.get()) / 10), self.Build)
        t.start()

    def Work(self):
        self.WorkInProgress = True
        timenow = time.time()
        diff = timenow - self.LastTime
        self.LastTime = timenow

        self.PercentWorked += diff / self.WorkTime * 100

        if self.PercentWorked >= 100:
            self.PercentWorked = 0
            self.WorkFin = True
            self.WorkInProgress = False
            self.WorkFinished()
            for actor in self.Wokers.values():
                self.RemoveActor(actor)
            return
        t = Timer(.5  /( float(self.DataStore.TimeScaling.get()) / 10), self.Work)
        t.start()

    def WorkFinished(self):
        for resource, value in self.WorkResourceProduce.iteritems():
            if value > 0:
                self.DataStore.Village.addResource([(resource, value)])
        return

    def BuildingFinished(self):
        return

    def waitForResources(self):
        if not self.Built:
            if self.DataStore.Village.requestResources(self.ResouceCost):
                self.LastTime = time.time()
                self.Build()        
                return
        else:
            if self.DataStore.Village.requestResources(self.WorkResourceCost):            
                self.WorkFin = False
                self.Work()
                return

        t = Timer(.25  / (float(self.DataStore.TimeScaling.get()) / 10), self.waitForResources)
        t.start()

    def WorkDone(self):
        return self.WorkFin and self.PercentWorked == 0 and not self.WorkInProgress