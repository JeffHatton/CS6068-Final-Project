from Actor import *
from Villlages.VillageRequest import *
import math
import time
from Villlages.Buildings.House import *
from Villlages.Buildings.StockPile import *
from Villlages.Buildings.ResourceProcessor import *


class NeedAnalyzer(Actor):
    """description of class"""

    def __init__(self, dataStore):
        self.DataStore = dataStore
        self.FoodStockPilePreference = 1.25
        self.FoodPerWorkerNeededNeeded = 20
        self.AverageHungerLimitForMore = 120
        self.RawStockPileLimit = 300
        self.StoreLimitForMore = 10
        self.AverageHunger = 0
        self.TotalConsumption = 1
        self.Counter = 0
        self.StoragePerStockPile = 200
        Actor.__init__(self, dataStore)

    def run(self):
        while not self.stop_requested:
            self.AnalyzeFood()
            self.AnalyzeMoreVillagers()
            self.idleProduction()
            self.MoreStockPiles()
            if self.Counter % 3 == 0:
                self.AnalyzeMoreHouses()


            self.Counter += 1
            #self.AnalyzeStockPiles()
            time.sleep(.5 / (float(self.DataStore.TimeScaling.get()) / 10))            

    def MoreStockPiles(self):
        if len(self.DataStore.findAllIdleReadBuildings("StockPile", self.DataStore.DoesBuildingExist)) < len(self.DataStore.EnvActors) / 10:
            id = self.DataStore.getBuildingPoint()
            self.DataStore.EnvTiles[id].Structure = StockPile(self.DataStore, self.DataStore.EnvTiles[id])
            self.DataStore.Village.addWant(VillageRequest("Build:{0}".format(id), 2), self.DataStore.EnvTiles[id].Structure.WokersRequiredToBuild)
            self.DataStore.AddBuilding(1)

    def AnalyzeMoreHouses(self):
        if len(self.DataStore.EnvActors) + 2 > self.DataStore.ProspectiveHousing:
            self.DataStore.Logger.addToLog("Length:{0}".format(int(math.ceil((len(self.DataStore.EnvActors) + 4 - self.DataStore.ProspectiveHousing) / 5.0))), 0)
            for x in range(0, int(math.ceil((len(self.DataStore.EnvActors) + 4 - self.DataStore.ProspectiveHousing) / 5.0))):
                id = self.DataStore.getBuildingPoint()
                self.DataStore.EnvTiles[id].Structure = House(self.DataStore, self.DataStore.EnvTiles[id])
                self.DataStore.Village.addWant(VillageRequest("Build:{0}".format(id), 2), self.DataStore.EnvTiles[id].Structure.WokersRequiredToBuild)
                self.DataStore.AddBuilding(1)
                self.DataStore.addProspective(5)

    def AnalyzeMoreVillagers(self):        
        if self.AverageHungerLimitForMore > self.AverageHunger and len(self.DataStore.EnvActors) + 1 <= self.DataStore.HousingAvilable:
            if self.DataStore.Village.Resources["Food"] / self.TotalConsumption > self.StoreLimitForMore:
                self.DataStore.Village.addWant(VillageRequest("Mate", 1), 2)


    def idleProduction(self):
        count = self.DataStore.findAllIdleReadBuildings("FoodProcessor", self.DataStore.isBuildingIdleandBuilt)
        for x in range(0,len(count)):
            self.DataStore.Village.addWant(VillageRequest("Refine:Food", 0), len(count))

    def AnalyzeFood(self):
        if len(self.DataStore.EnvActors) == 0:
            return

        averageHunger = 0
        averageFoodHunger = 0
        totalFoodNeeded = 0
        averageConsumption = 0
        for key,actor in self.DataStore.EnvActors.iteritems():
            averageHunger += actor.Hunger
            totalFoodNeeded += actor.Hunger / actor.FoodToHungerConversion
            averageFoodHunger += actor.FoodToHungerConversion
            averageConsumption += actor.HungerDisRate
        diffFoods = (self.FoodStockPilePreference * totalFoodNeeded) - self.DataStore.Village.Resources["Food"] 
        if diffFoods > 0:
            workersNeeded = int(math.ceil(diffFoods / self.FoodPerWorkerNeededNeeded))            
            idx = self.DataStore.findIdle("FoodProcessor")

            if idx == -1:
                id = self.DataStore.getBuildingPoint()
                self.DataStore.EnvTiles[id].Structure = FoodProcessor(self.DataStore, self.DataStore.EnvTiles[id])
                self.DataStore.Village.addWant(VillageRequest("Build:{0}".format(id), 2), self.DataStore.EnvTiles[id].Structure.WokersRequiredToBuild)
                self.DataStore.AddBuilding(1)
            else:
                count = self.DataStore.findAllIdleReadBuildings("FoodProcessor", self.DataStore.isBuildingIdleandBuilt)
                for x in range(0,len(count)):
                    self.DataStore.Village.addNeed(VillageRequest("Refine:Food", 0), len(count))
                self.DataStore.Village.addNeed(VillageRequest("Gather:Food", 0), workersNeeded - len(count))
      
        self.AverageHunger = averageHunger / len(self.DataStore.EnvActors)
        self.TotalConsumption = averageConsumption

    def AnalyzeStockPiles(self):
        totalResources = 0
        for res in self.DataStore.Village.Resources.keys():
            totalResources += self.DataStore.Village.Resources[res]
        
        if totalResources > (self.DataStore.StockPiles + self.DataStore.ProspectiveStockPiles) * self.StoragePerStockPile:
            while True:
                id = random.randint(0, (self.DataStore.EnvironmentDimX * self.DataStore.EnvironmentDimY)-1)
                if self.DataStore.EnvTiles[id].ResourceType == "None":
                    self.DataStore.EnvTiles[id].Structure = Villlages.Buildings.StockPile.StockPile(self.DataStore, self.DataStore.EnvTiles[id])
                    self.DataStore.Village.addNeed(VillageRequest("Build:{0}".format(id), 0), 2)
                    self.DataStore.addProspectiveStockPile()
                    break
