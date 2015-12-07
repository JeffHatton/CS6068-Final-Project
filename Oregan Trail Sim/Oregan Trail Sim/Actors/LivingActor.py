from Actor import *
from Data.DataStore import *
import math
import time
from threading import Timer
import heapq

class LivingActor(Actor):
    """description of class"""
    
    def __init__(self, dataStore, tile):
        Actor.__init__(self, dataStore)
        self.CurrentTile = tile
        self.CurrentTile.AddActor(self)
        self.HP = 0
        self.CarryLimit = 25
        self.CurrentInvCount = 0;
        self.Inventory = dict()      
        for resource in dataStore.AllResources():
            self.Inventory[resource] = 0
              
        self.HungerLock = threading.Lock()
        self.CriticalFoodLimit = 90
        self.AllowHungerToIncrease = True
        self.FoodGetLimit = 30

        # Status of the actor
        self.Status = "Healthy"

        # Limit of hunger before actor dies
        self.HungerLimit = 200

        # How hungry the actor is
        self.Hunger = 0

        # How quickly actor gets hungry hunger/s
        self.HungerDisRate = .5

        # Tiles/s
        self.MoveSpeed = 2
        
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

    def getSuccessors(self, Node):
        (path, (X,Y)) = Node
        result = []
        idEast = self.DataStore.TileIdConverter.Convert2dTo1d(X + 1, Y)
        idWest = self.DataStore.TileIdConverter.Convert2dTo1d(X - 1, Y)
        idNorth = self.DataStore.TileIdConverter.Convert2dTo1d(X, Y + 1)
        idSouth = self.DataStore.TileIdConverter.Convert2dTo1d(X, Y - 1)

        idNorthEast = self.DataStore.TileIdConverter.Convert2dTo1d(X + 1, Y + 1)
        idNorthWest = self.DataStore.TileIdConverter.Convert2dTo1d(X - 1, Y + 1)
        idSouthEast = self.DataStore.TileIdConverter.Convert2dTo1d(X + 1, Y - 1)
        idSouthWest = self.DataStore.TileIdConverter.Convert2dTo1d(X - 1, Y - 1)

        if idEast >= 0 and self.DataStore.EnvTiles[idEast].Walkable:
            result.append((path + [self.DataStore.TileIdConverter.Convert2dTo1d(X+1,Y)], (X+1, Y)))
        if idWest >= 0 and self.DataStore.EnvTiles[idWest].Walkable:
            result.append((path + [self.DataStore.TileIdConverter.Convert2dTo1d(X-1,Y)], (X-1, Y)))
        if idNorth >= 0 and self.DataStore.EnvTiles[idNorth].Walkable:
            result.append((path + [self.DataStore.TileIdConverter.Convert2dTo1d(X,Y+1)], (X, Y+1)))
        if idSouth >= 0 and self.DataStore.EnvTiles[idSouth].Walkable:
            result.append((path + [self.DataStore.TileIdConverter.Convert2dTo1d(X,Y-1)], (X, Y-1)))
        
        if idNorthEast >= 0 and self.DataStore.EnvTiles[idNorthEast].Walkable:
            result.append((path + [self.DataStore.TileIdConverter.Convert2dTo1d(X+1,Y+1)], (X+1, Y+1)))
        if idNorthWest >= 0 and self.DataStore.EnvTiles[idNorthWest].Walkable:
            result.append((path + [self.DataStore.TileIdConverter.Convert2dTo1d(X-1,Y+1)], (X-1, Y+1)))
        if idSouthEast >= 0 and self.DataStore.EnvTiles[idSouthEast].Walkable:
            result.append((path + [self.DataStore.TileIdConverter.Convert2dTo1d(X+1,Y-1)], (X+1, Y-1)))
        if idSouthWest >= 0 and self.DataStore.EnvTiles[idSouthWest].Walkable:
            result.append((path + [self.DataStore.TileIdConverter.Convert2dTo1d(X-1,Y-1)], (X-1, Y-1)))
        
        return result

    def goalHeuristic(self, Node, Destination):
        (path, (Cx, Cy)) = Node
        (Dx, Dy) = Destination
        return math.sqrt(pow(Cx - Dx, 2) + pow(Cy - Dy, 2));

    # TODO: Basic, but functional.
    def aStarPathSearch(self, tileId):
        (desX, desY) = self.DataStore.TileIdConverter.Convert1dTo2d(tileId)
        (curX, curY) = self.DataStore.TileIdConverter.Convert1dTo2d(self.CurrentTile.ID.LocalId)

        frontier = []
        heapq.heappush( frontier, (self.goalHeuristic(([], (curX, curY)), (desX, desY)), ([], (curX, curY))) )
        explored = {}
        while len(frontier) > 0:
            (priority, curNode) = heapq.heappop(frontier)
            if str(curNode[1]) in explored:
                continue
            explored[str(curNode[1])] = 1
            for testnode in self.getSuccessors(curNode):
                if testnode[1][0] == desX and testnode[1][1] == desY:
                    return testnode[0]
                if str(testnode[1]) in explored:
                    continue
                heapq.heappush(frontier, (len(testnode[0]) + self.goalHeuristic(testnode, (desX,desY)), testnode))
        return []

    def determinePath(self, tileId):
        return self.aStarPathSearch(tileId)

    def depositResouce(self, resourceType):
        #path to store house
        if resourceType in self.Inventory.keys():
            if self.Inventory[resourceType] > 0:                
                self.DataStore.Village.addResource([(resourceType, self.Inventory[resourceType])])
                self.AddInventory(resourceType, -self.Inventory[resourceType])

    def depositAllResources(self):
        resourceChangeRequest = list()
        self.DataStore.Logger.addToLog(self.Inventory, 10)
        for resource in  self.DataStore.AllResources():
            if resource in self.Inventory.keys():
                if self.Inventory[resource] > 0:
                    resourceChangeRequest.append((resource, self.Inventory[resource]))
                    self.AddInventory(resource, -self.Inventory[resource])
        if len(resourceChangeRequest) > 0:
            self.DataStore.Village.addResource(resourceChangeRequest)

    def getFood(self):
        self.CurrentTask = "GetFood"
        self.eat()
        foodneeded = int(math.ceil(self.Hunger / self.FoodToHungerConversion))
        foodAmount = self.DataStore.Village.requestResource("Food", foodneeded, False)
        self.AddInventory("Food", foodAmount)

    def eat(self):
        self.HungerLock.acquire()
        self.DataStore.Logger.addToLog("Actor {0} Old Hunger {1}".format(self.ID.GUID, self.Hunger), 6)
        self.Hunger -=  self.Inventory["Food"] * self.FoodToHungerConversion
        if self.Hunger < 0:
            self.Hunger = 0
        self.DataStore.Logger.addToLog("Actor {0} New Hunger {1}".format(self.ID.GUID, self.Hunger), 0)
        self.HungerLock.release()
        self.AddInventory("Food", -self.Inventory["Food"])
        self.CurrentTask = "Idle"
    
    def StatusCheck(self):
        if self.Hunger > self.HungerLimit:
            self.Status = "Dead"
            return

    def hungerChecker(self):
        if self.AllowHungerToIncrease:
            timenow = time.time()
            diff = timenow - self.LastTime
            self.LastTime = timenow
            self.HungerLock.acquire()
            self.Hunger += diff * self.HungerDisRate
            self.HungerLock.release()
            self.DataStore.Logger.addToLog("Actor {0} Auto Hunger {1} Task {2}".format(self.ID.GUID, self.Hunger, self.CurrentTask), 5)
        else:
            self.LastTime = time.time()
        t = Timer(1, self.hungerChecker)
        t.start()

    def AddInventory(self, resourceType, amount):

        if amount + self.CurrentInvCount > self.CarryLimit:
            amount = CarryLimit - self.CurrentInvCount

        if resourceType in self.Inventory.keys():
            self.CurrentInvCount += amount
            self.Inventory[resourceType] += amount
        else:
            self.CurrentInvCount += amount
            self.Inventory[resourceType] = amount
