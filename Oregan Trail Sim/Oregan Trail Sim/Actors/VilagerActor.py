from LivingActor import *
import random
import time

class VilagerActor(LivingActor):
    """description of class"""

    def __init__(self, dataStore, tile):
        LivingActor.__init__(self, dataStore, tile)

        gather = random.randint(0,2)
        self.PreferedAction = "Gather"
        self.gatherRandomResource()                                    

    def run(self):        
        while True:                
            threadSleepTime = random.randint(500, 3000) / 1000

            # Check if Villager is alive
            self.StatusCheck()
            if self.Status == "Dead":
                self.CurrentTile.RemoveActor(self)
                self.DataStore.Logger.addToLog("Villager {0} has died.".format(self.ID.GUID), 0)
                del self.DataStore.EnvActors[self.ID.GUID]
                return
                                               
            if self.Hunger >= self.CriticalFoodLimit:
                self.CurrentTask = "GetFood"

            self.DataStore.Logger.addToLog("Actor {0} doing Task {1} with Action {2}".format(self.ID.GUID, self.CurrentTask, self.CurrentAction), 5)
            if self.CurrentTask.startswith("Gather:"):                               
                if self.CurrentAction == "Idle":
                    id = self.findNearestResourceTile(self.CurrentTask[7:])
                    if id > -1:
                        self.DataStore.Logger.addToLog(("Trying to move to {0} Tile Type: {1} From {2}").format(id, self.DataStore.EnvTiles[id].ResourceType, self.CurrentTile.ID.LocalId), 5)
                        if self.DataStore.EnvTiles[id].Walkable:                                       
                            self.CurrentMovePath = self.determinePath(id)                                
                            self.DataStore.Logger.addToLog(("Taking path {0}").format(self.CurrentMovePath),5)
                            self.CurrentAction = "Moving"
                            continueLoop = False     
                elif self.CurrentAction == "Moving":
                    if len(self.CurrentMovePath) == 0:
                        self.CurrentAction = "Gather"
                        self.DataStore.Logger.addToLog(("Reached Dest {0} start gathering").format(self.CurrentTile.ID.LocalId), 5)
                    else:
                        movePoint = self.CurrentMovePath.pop(0)
                        self.MoveTo(self.DataStore.EnvTiles[movePoint])                        
                        threadSleepTime = 1 / self.MoveSpeed
                        self.DataStore.Logger.addToLog(("Moving to {0} wating {1} s before moving again").format(movePoint, threadSleepTime), 4)
                elif self.CurrentAction == "Gather":
                    self.GatherFromTile()
                    self.depositAllResources()
                    self.CurrentAction = "Idle"
                    self.CurrentTask = "Idle"
                    self.DataStore.Logger.addToLog(("Gathering"), 4)
            elif self.CurrentTask == "Idle":
                if self.Hunger > self.FoodGetLimit:
                    self.getFood()
                    self.eat()
                self.CurrentTask = self.DataStore.Village.giveWork()
            elif self.CurrentTask == "GetFood":
                self.getFood()
                self.eat()
                self.CurrentTask = "Idle"

            #self.Hunger += random.randint(0,2)
            self.DataStore.Logger.addToLog("Sleeping for {0}".format(threadSleepTime), 5)
            time.sleep(threadSleepTime)

    def GatherFromTile(self):
        self.DataStore.Logger.addToLog(("Attempting to gather from {0} Tile").format(self.CurrentTile.ResourceType), 4)
        if self.CurrentTile.ResourceType != "None":
            if self.CurrentTile.ResourceType in self.Inventory.keys():
                self.Inventory[self.CurrentTile.ResourceType] += self.CarryLimit                        
            else:
                self.Inventory[self.CurrentTile.ResourceType] = self.CarryLimit
            
    def findNearestResourceTile(self, resourceType):        
        tileId = -1
        self.DataStore.Logger.addToLog(("Trying to find {0} Tile").format(resourceType), 4)
        for searchDistance in range(1,10):
            for x in range(-searchDistance, searchDistance):
                id = self.DataStore.TileIdConverter.Convert2dTo1d(self.CurrentTile.ID.IdX + x, self.CurrentTile.ID.IdY + searchDistance)
                if id >= 0:
                    self.DataStore.Logger.addToLog(("Examining {0} Type: {1}").format(id, self.DataStore.EnvTiles[id].ResourceType), 8)
                    if self.DataStore.EnvTiles[id].ResourceType == resourceType:
                        return id
                        tileId = id
                        break;
                id = self.DataStore.TileIdConverter.Convert2dTo1d(self.CurrentTile.ID.IdX + x, self.CurrentTile.ID.IdY -searchDistance)
                if id >= 0:
                    self.DataStore.Logger.addToLog(("Examining {0} Type: {1}").format(id, self.DataStore.EnvTiles[id].ResourceType), 8)
                    if self.DataStore.EnvTiles[id].ResourceType == resourceType:
                        return id
                        tileId = id
                        break;
            for y in range(-searchDistance, searchDistance):
                id = self.DataStore.TileIdConverter.Convert2dTo1d(self.CurrentTile.ID.IdX + searchDistance, self.CurrentTile.ID.IdY + y)
                if id >= 0:
                    self.DataStore.Logger.addToLog(("Examining {0} Type: {1}").format(id, self.DataStore.EnvTiles[id].ResourceType), 8)
                    if self.DataStore.EnvTiles[id].ResourceType == resourceType:
                        return id
                        tileId = id
                        break;
                id = self.DataStore.TileIdConverter.Convert2dTo1d(self.CurrentTile.ID.IdX -searchDistance, self.CurrentTile.ID.IdY + y)
                if id >= 0:
                    self.DataStore.Logger.addToLog(("Examining {0} Type: {1}").format(id, self.DataStore.EnvTiles[id].ResourceType), 8)
                    if self.DataStore.EnvTiles[id].ResourceType == resourceType:
                        return id
                        tileId = id
                        break;
        self.DataStore.Logger.addToLog(("Found Tile {0}").format(tileId), 4)
        return tileId

    def moveToRandomTile(self):
        continueLoop = True       
        while continueLoop:
            tileId = random.randint(0,99)                
            self.DataStore.Logger.addToLog(("Trying to move to {0} Tile Type: {1} From {2}").format(tileId, self.DataStore.EnvTiles[tileId].ResourceType, self.CurrentTile.ID.LocalId), 4)
            if self.DataStore.EnvTiles[tileId].Walkable:                                       
                self.CurrentMovePath = self.determinePath(tileId)                                
                self.DataStore.Logger.addToLog(("Taking path {0}").format(self.CurrentMovePath) , 4)
                self.CurrentAction = "Moving"
                continueLoop = False

    def gatherRandomResource(self):
        self.CurrentTask = ["Gather:Wood", "Gather:Food", "Gather:Stone"][random.randint(0,2)]

