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
            if self.CurrentTask.startswith("Gather:"):                               
                if self.CurrentAction == "Idle":
                    id = self.findNearestResourceTile(self.CurrentTask[7:])
                    if id > -1:
                        print("Trying to move to {0} Tile Type: {1} From {2}").format(id, self.DataStore.EnvTiles[id].ResourceType, self.CurrentTile.ID.LocalId)
                        if self.DataStore.EnvTiles[id].Walkable:                                       
                            self.CurrentMovePath = self.determinePath(id)                                
                            print("Taking path {0}").format(self.CurrentMovePath)
                            self.CurrentAction = "Moving"
                            continueLoop = False     
                elif self.CurrentAction == "Moving":
                    if len(self.CurrentMovePath) == 0:
                        self.CurrentAction = "Gather"
                        print("Reached Dest {0} start gathering").format(self.CurrentTile.ID.LocalId)
                    else:
                        movePoint = self.CurrentMovePath.pop(0)
                        self.MoveTo(self.DataStore.EnvTiles[movePoint])                        
                        threadSleepTime = 1 / self.MoveSpeed
                        print("Moving to {0} wating {1} s before moving again").format(movePoint, threadSleepTime)
                elif self.CurrentAction == "Gather":
                    self.GatherFromTile()
                    self.depositAllResources()
                    self.CurrentAction = "Idle"
                    self.gatherRandomResource()
                    print("Gathering")

            time.sleep(threadSleepTime)

    def GatherFromTile(self):
        print("Attempting to gather from {0} Tile").format(self.CurrentTile.ResourceType)
        if self.CurrentTile.ResourceType != "None":
            if self.CurrentTile.ResourceType in self.Inventory.keys():
                self.Inventory[self.CurrentTile.ResourceType] += self.CarryLimit                        
            else:
                self.Inventory[self.CurrentTile.ResourceType] = self.CarryLimit
            
    def findNearestResourceTile(self, resourceType):        
        tileId = -1
        print("Trying to find {0} Tile").format(resourceType)
        for searchDistance in range(1,10):
            for x in range(-searchDistance, searchDistance):
                id = self.DataStore.TileIdConverter.Convert2dTo1d(self.CurrentTile.ID.IdX + x, searchDistance)
                if id >= 0:
                    if self.DataStore.EnvTiles[id].ResourceType == resourceType:
                        tileId = id
                        break;
                id = self.DataStore.TileIdConverter.Convert2dTo1d(self.CurrentTile.ID.IdX + x, -searchDistance)
                if id >= 0:
                    if self.DataStore.EnvTiles[id].ResourceType == resourceType:
                        tileId = id
                        break;
            for y in range(-searchDistance, searchDistance):
                id = self.DataStore.TileIdConverter.Convert2dTo1d(searchDistance, self.CurrentTile.ID.IdY + y)
                if id >= 0:
                    if self.DataStore.EnvTiles[id].ResourceType == resourceType:
                        tileId = id
                        break;
                id = self.DataStore.TileIdConverter.Convert2dTo1d(-searchDistance, self.CurrentTile.ID.IdY + y)
                if id >= 0:
                    if self.DataStore.EnvTiles[id].ResourceType == resourceType:
                        tileId = id
                        break;
        print("Found Tile {0}").format(tileId)
        return tileId

    def moveToRandomTile(self):
        continueLoop = True       
        while continueLoop:
            tileId = random.randint(0,99)                
            print("Trying to move to {0} Tile Type: {1} From {2}").format(tileId, self.DataStore.EnvTiles[tileId].ResourceType, self.CurrentTile.ID.LocalId)
            if self.DataStore.EnvTiles[tileId].Walkable:                                       
                self.CurrentMovePath = self.determinePath(tileId)                                
                print("Taking path {0}").format(self.CurrentMovePath)
                self.CurrentAction = "Moving"
                continueLoop = False

    def gatherRandomResource(self):
        self.CurrentTask = ["Gather:Wood", "Gather:Wood", "Gather:Wood"][random.randint(0,2)]
