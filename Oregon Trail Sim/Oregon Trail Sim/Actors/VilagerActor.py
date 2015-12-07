from LivingActor import *
import random
import time
from Data.DataStore import *

class VilagerActor(LivingActor):
    """description of class"""

    def __init__(self, dataStore, tile):
        LivingActor.__init__(self, dataStore, tile)

        gather = random.randint(0,2)
        self.PreferedAction = "Gather"
        self.ThreadSleepTime = 0

    def run(self):
        while not self.stop_requested:
            self.ThreadSleepTime = random.randint(1000, 1000) / 1000

            # Check if Villager is alive
            self.StatusCheck()
            if self.Status == "Dead":
                self.CurrentTile.RemoveActor(self)
                self.DataStore.Logger.addToLog("Villager {0} has died.".format(self.ID.GUID), 0)
                self.DataStore.RemoveActor(self.ID.GUID)
                return

            if self.Hunger >= self.CriticalFoodLimit:
                self.CurrentTask = "GetFood"
                self.DataStore.Logger.addToLog("Actor {0} Critical Food Limit".format(self.ID.GUID), 0)

            self.DataStore.Logger.addToLog("Actor {0} doing Task {1} with Action {2}".format(self.ID.GUID, self.CurrentTask, self.CurrentAction), 5)
            if self.CurrentTask.startswith("Build:"):
                self.HandleBuildTask()
            if self.CurrentTask.startswith("Gather:"):
                self.HandleGatherTask()
            if self.CurrentTask.startswith("Refine:"):
                self.handleRefine()
            elif self.CurrentTask == "Idle":
                self.HandleIdleTask()
            elif self.CurrentTask == "GetFood":
                self.HandleGetFoodTask()
            elif self.CurrentTask == "Deposit":
                self.HandleDepositResources()
            elif self.CurrentTask == "Mate":
                self.HandleMate()

            #self.DataStore.Logger.addToLog("Sleeping for {0}".format(self.ThreadSleepTime * float(self.DataStore.TimeScaling)), 5)
            time.sleep(self.ThreadSleepTime / (float(self.DataStore.TimeScaling) / 10))

    def GatherFromTile(self):
        self.DataStore.Logger.addToLog(("Attempting to gather from {0} Tile").format(self.CurrentTile.ResourceType), 4)
        if self.CurrentTile.ResourceType != "None":
            self.AddInventory(self.CurrentTile.ResourceType, self.CurrentTile.GatherAmountGiven)

    def findNearestResourceTile(self, resourceType):
        return self.searchTiles(resourceType, lambda tile, searchValue: tile.ResourceType == searchValue)

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
        allResources = self.DataStore.AllResourcesgatherableResources()
        self.CurrentTask = "Gather:" + allResources[random.randint(0,len(allResources) - 1)]

    def Move(self):
        if len(self.CurrentMovePath) > 0:
            movePoint = self.CurrentMovePath.pop(0)
            self.MoveTo(self.DataStore.EnvTiles[movePoint])
            self.ThreadSleepTime = 1 / self.MoveSpeed
            self.DataStore.Logger.addToLog(("Moving to {0} wating {1} s before moving again").format(movePoint, self.ThreadSleepTime), 4)
        return len(self.CurrentMovePath)

    def HandleBuildTask(self):
        if self.CurrentAction == "Idle":
            id = self.CurrentTask[6:]
            self.CurrentMovePath = self.determinePath(int(id))
            self.DataStore.Logger.addToLog(("Taking path {0}").format(self.CurrentMovePath),2)
            self.CurrentAction = "Moving"
        if self.CurrentAction == "Moving":
            if self.Move() == 0:
                self.CurrentAction = "Build"
                self.DataStore.Logger.addToLog(("Reached Dest {0} start Building").format(self.CurrentTile.ID.LocalId), 3)
                self.CurrentTile.Structure.AddActor(self)
        if self.CurrentAction == "Build":
            self.AllowHungerToIncrease = False
            if self.CurrentTile.Structure.PercentBuilt == 100:
                self.idleWork()
                self.AllowHungerToIncrease = True

    def HandleGatherTask(self):
        if self.CurrentAction == "Idle":
            id = self.findNearestResourceTile(self.CurrentTask[7:])
            self.DataStore.Logger.addToLog(("Tile {0}").format(id), 6)
            if id > -1:
                self.findPath(id)
        elif self.CurrentAction == "Moving":
            if self.Move() == 0:
                self.CurrentAction = "Gather"
                self.DataStore.Logger.addToLog(("Reached Dest {0} start gathering").format(self.CurrentTile.ID.LocalId), 5)
        elif self.CurrentAction == "Gather":
            self.GatherFromTile()
            self.ThreadSleepTime = self.CurrentTile.GatherTime
            if self.CurrentInvCount == self.CarryLimit:
                self.CurrentTask = "Deposit"
            elif self.DataStore.Village.VillageHasNeeds():
                self.CurrentTask = "Idle"
            self.CurrentAction = "Idle"
            self.DataStore.Logger.addToLog(("Gathering"), 4)

    def HandleIdleTask(self):
        if self.Hunger > self.FoodGetLimit:
            self.getFood()
            self.eat()
        self.CurrentTask = self.DataStore.Village.giveWork()

    def HandleGetFoodTask(self):
        self.getFood()
        self.eat()
        self.CurrentTask = "Idle"

    def isBuildingType(self, tile, buildingType):
        if tile.Structure != None:
            if tile.Structure.BuildingType == buildingType:
                return True
        return False

    def HandleDepositResources(self):
        if self.CurrentAction == "Idle":
            tileId = self.searchTiles("StockPile", self.isBuildingType)
            if tileId >= 0:
                self.findPath(tileId)
        if self.CurrentAction == "Moving":
            if self.Move() == 0:
                self.CurrentAction = "Deposit"
                self.DataStore.Logger.addToLog(("Reached Dest {0} start gathering").format(self.CurrentTile.ID.LocalId), 5)
        if self.CurrentAction == "Deposit":
            if self.CurrentTile.Structure.BuildingType == "StockPile":
                self.depositAllResources()
                self.idleWork()
            else:
                self.CurrentAction = "Idle"

    def searchTiles(self, searchValue, searchFunction):
        tileId = -1

        if  searchFunction(self.CurrentTile, searchValue):
            return self.CurrentTile.ID.LocalId

        for searchDistance in range(1,self.DataStore.x):
            for x in range(-searchDistance, searchDistance):
                id = self.DataStore.TileIdConverter.Convert2dTo1d(self.CurrentTile.ID.IdX + x, self.CurrentTile.ID.IdY + searchDistance)
                if id >= 0:
                    if  searchFunction(self.DataStore.EnvTiles[id], searchValue):
                        return id
                id = self.DataStore.TileIdConverter.Convert2dTo1d(self.CurrentTile.ID.IdX + x, self.CurrentTile.ID.IdY -searchDistance)
                if id >= 0:
                    if searchFunction(self.DataStore.EnvTiles[id], searchValue):
                        return id
            for y in range(-searchDistance, searchDistance):
                id = self.DataStore.TileIdConverter.Convert2dTo1d(self.CurrentTile.ID.IdX + searchDistance, self.CurrentTile.ID.IdY + y)
                if id >= 0:
                    if searchFunction(self.DataStore.EnvTiles[id], searchValue):
                        return id
                id = self.DataStore.TileIdConverter.Convert2dTo1d(self.CurrentTile.ID.IdX -searchDistance, self.CurrentTile.ID.IdY + y)
                if id >= 0:
                    if searchFunction(self.DataStore.EnvTiles[id], searchValue):
                        return id
        return tileId

    def findPath(self, id):
        self.DataStore.Logger.addToLog(("Trying to move to {0} Tile Type: {1} From {2}").format(id, self.DataStore.EnvTiles[id].ResourceType, self.CurrentTile.ID.LocalId), 5)
        self.CurrentMovePath = self.determinePath(id)
        self.DataStore.Logger.addToLog(("Taking path {0}").format(self.CurrentMovePath),5)
        self.CurrentAction = "Moving"

    def idleWork(self):
        self.CurrentTask = "Idle"
        self.CurrentAction = "Idle"

    def HandleMate(self):
        if self.CurrentAction == "Idle":
            tileId = self.searchTiles("House", self.findIdleBuilding)
            if tileId >= 0:
                self.findPath(tileId)
        if self.CurrentAction == "Moving":
            if self.Move() == 0:
                if self.CurrentTile.Structure.WorkInProgress:
                    self.CurrentAction = "Idle"
                else:
                    self.CurrentAction = "Mate"
                    self.CurrentTile.Structure.AddActor(self)
        if self.CurrentAction == "Mate":
            self.AllowHungerToIncrease = False
            self.DataStore.Logger.addToLog("Actor {1} Mating: {0}".format(self.CurrentTile.Structure.WorkFin, self.ID.GUID),5)
            if self.CurrentTile.Structure.WorkFin:
                self.DataStore.Logger.addToLog("Done Actor {1} Mating: {0}".format(self.CurrentTile.Structure.WorkFin, self.ID.GUID),5)
                self.AllowHungerToIncrease = True
                self.idleWork()

    def findIdleBuilding(self, tile, buildingType):
        if tile.Structure != None:
            if tile.Structure.BuildingType == buildingType and not tile.Structure.WorkInProgress and tile.Structure.Built:
                return True
        return False
    def handleRefine(self):
        if self.CurrentAction == "Idle":
            self.DataStore.Logger.addToLog(self.CurrentTask[7:],2)
            tileId = self.DataStore.findIdle(self.DataStore.refineMap[self.CurrentTask[7:]])
            if tileId >= 0:
                self.findPath(tileId)
        if self.CurrentAction == "Moving":
            if self.Move() == 0:
                if self.CurrentTile.Structure.WorkInProgress:
                    self.CurrentAction = "Idle"
                else:
                    self.CurrentAction = "Work"
                    self.CurrentTile.Structure.AddActor(self)
        if self.CurrentAction == "Work":
            self.AllowHungerToIncrease = False
            if self.CurrentTile.Structure.WorkFin:
                self.AllowHungerToIncrease = True
                self.idleWork()
