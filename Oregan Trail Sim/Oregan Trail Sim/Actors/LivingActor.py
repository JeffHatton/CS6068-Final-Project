from Actor import *
from Data.DataStore import *
import math

class LivingActor(Actor):
    """description of class"""
    
    def __init__(self, dataStore, tile):
        Actor.__init__(self, dataStore)
        self.CurrentTile = tile
        self.CurrentTile.AddActor(self)
        self.HP = 0
        self.CarryLimit = 5
        self.Inventory = dict()

        # How hungry the actor is
        self.Hunger = 0

        # How quickly actor gets hungry hunger/s
        self.HungerDisRate = 1

        # Tiles/s
        self.MoveSpeed = .25
        
        self.CurrentMovePath = list()

        # Conversion factor for food to hunger
        self.FoodToHungerConversion = 1

    def MoveTo(self, Tile):
        self.CurrentTile.RemoveActor(self)
        self.CurrentTile = Tile
        Tile.AddActor(self)

    def determinePath(self, tileId):
        (desX, desY) = self.DataStore.TileIdConverter.Convert1dTo2d(tileId)
        (curX, curY) = self.DataStore.TileIdConverter.Convert1dTo2d(self.CurrentTile.ID.LocalId)
        
        path = list()
        print("Attempting to find path to {0}").format((desX, desY))
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
            print("Adding {0} to path").format(self.DataStore.TileIdConverter.Convert2dTo1d(curX,curY))
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
        print(self.Inventory)
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
        self.Inventory["Food"] = self.DataStore.Village.requestResource("Food", foodneeded)

    def eat(self):
        self.Hunger -=  self.Inventory["Food"] * self.FoodToHungerConversion
        self.Inventory["Food"] = 0
    



