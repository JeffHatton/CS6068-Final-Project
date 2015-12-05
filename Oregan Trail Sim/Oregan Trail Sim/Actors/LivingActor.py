from Actor import *
from Data.DataStore import *
import math
import time
import timer

class LivingActor(Actor):
    """description of class"""
    
    def __init__(self, dataStore, tile):
        Actor.__init__(self, dataStore)
        self.CurrentTile = tile
        self.CurrentTile.AddActor(self)
        self.HP = 0
        self.CarryLimit = 25
        self.Inventory = dict()        
        self.HungerLock = threading.Lock()
        self.CriticalFoodLimit = 75
        self.FoodGetLimit = 50

        # Status of the actor
        self.Status = "Healthy"

        # Limit of hunger before actor dies
        self.HungerLimit = 100

        # How hungry the actor is
        self.Hunger = 0

        # How quickly actor gets hungry hunger/s
        self.HungerDisRate = 10

        # Tiles/s
        self.MoveSpeed = .25
        
        self.CurrentMovePath = list()

        # Conversion factor for food to hunger
        self.FoodToHungerConversion = 10        

    def MoveTo(self, Tile):
        self.CurrentTile.RemoveActor(self)
        self.CurrentTile = Tile
        Tile.AddActor(self)


    def start(self):
        self.LastTime = time.time()
        self.hungerChecker()
        Thread.start(self)

    def determinePath(self, tileId):
        (desX, desY) = self.DataStore.TileIdConverter.Convert1dTo2d(tileId)
        (curX, curY) = self.DataStore.TileIdConverter.Convert1dTo2d(self.CurrentTile.ID.LocalId)
        
        path = list()
        self.DataStore.Logger.addToLog("Attempting to find path to {0}".format((desX, desY)), 4)
        while curX != desX or curY != desY:            
            if curX < desX:
                if self.DataStore.EnvTiles[self.DataStore.TileIdConverter.Convert2dTo1d(curX + 1, curY)].Walkable:
                    curX = curX + 1
            elif curX > desX:
                if self.DataStore.EnvTiles[self.DataStore.TileIdConverter.Convert2dTo1d(curX - 1, curY)].Walkable:
                    curX = curX - 1

            if curY < desY:
                if self.DataStore.EnvTiles[self.DataStore.TileIdConverter.Convert2dTo1d(curX, curY + 1)].Walkable:
                    curY = curY + 1
            elif curY > desY:
                if self.DataStore.EnvTiles[self.DataStore.TileIdConverter.Convert2dTo1d(curX, curY - 1)].Walkable:
                    curY = curY - 1           

            path.append(self.DataStore.TileIdConverter.Convert2dTo1d(curX,curY))
            self.DataStore.Logger.addToLog("Adding {0} to path".format(self.DataStore.TileIdConverter.Convert2dTo1d(curX,curY)), 4)
        return path

    def depositResouce(self, resourceType):
        #path to store house
        if resourceType in self.Inventory:
            if self.Inventory[resourceType] > 0:                
                self.DataStore.Village.addResource([(resourceType, self.Inventory[resourceType])])
                self.Inventory[resourceType] = 0

    def depositAllResources(self):
        resourcesToDeposit = ["Food", "Stone", "Wood"]
        resourceChangeRequest = list()
        self.DataStore.Logger.addToLog(self.Inventory, 6)
        for resource in resourcesToDeposit:
            if resource in self.Inventory.keys():
                if self.Inventory[resource] > 0:
                    resourceChangeRequest.append((resource, self.Inventory[resource]))
                    self.Inventory[resource] = 0
        if len(resourceChangeRequest) > 0:
            self.DataStore.Village.addResource(resourceChangeRequest)

    def getFood(self):
        self.CurrentTask = "GetFood"
        foodneeded = int(math.ceil(self.Hunger / self.FoodToHungerConversion))
        self.Inventory["Food"] = self.DataStore.Village.requestResource("Food", foodneeded, False)

    def eat(self):
        self.HungerLock.acquire()
        self.DataStore.Logger.addToLog("Actor {0} Old Hunger {1}".format(self.ID.GUID, self.Hunger), 0)
        self.Hunger -=  self.Inventory["Food"] * self.FoodToHungerConversion
        if self.Hunger < 0:
            self.Hunger = 0
        self.DataStore.Logger.addToLog("Actor {0} New Hunger {1}".format(self.ID.GUID, self.Hunger), 0)
        self.HungerLock.release()
        self.Inventory["Food"] = 0
        self.CurrentTask = "Idle"
    
    def StatusCheck(self):
        if self.Hunger > self.HungerLimit:
            self.Status = "Dead"
            return

    def hungerChecker(self):
        timenow = time.time()
        diff = timenow - self.LastTime
        self.LastTime = timenow
        self.HungerLock.acquire()
        self.Hunger += diff * self.HungerDisRate
        self.HungerLock.release()
        self.DataStore.Logger.addToLog("Actor {0} Auto Hunger {1} Task {2}".format(self.ID.GUID, self.Hunger, self.CurrentTask), 0)
        t = Timer(1, self.hungerChecker)
        t.start()