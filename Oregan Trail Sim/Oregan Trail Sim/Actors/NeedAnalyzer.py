﻿from Actor import *
from Villlages.VillageRequest import *
import math
import time
from Villlages.Buildings.House import *


class NeedAnalyzer(Actor):
    """description of class"""

    def __init__(self, dataStore):
        self.DataStore = dataStore
        self.FoodStockPilePreference = 1.25
        self.FoodPerWorkerNeededNeeded = 20
        self.AverageHungerLimitForMore = 40
        self.StoreLimitForMore = 4
        self.AverageHunger = 0
        self.TotalConsumption = 1
        self.Counter = 0
        self.StoragePerStockPile = 200
        Actor.__init__(self, dataStore)

    def run(self):
        while not self.stop_requested:
            self.AnalyzeFood()
            self.AnalyzeMoreVillagers()
            self.AnalyzeMoreHouses()
            #if self.Counter % 3 == 0:
            #    self.AnalyzeMoreHouses()

            self.Counter += 1
            self.AnalyzeStockPiles()
            time.sleep(10)            

    def AnalyzeMoreHouses(self):
        if len(self.DataStore.EnvActors) + 4 > self.DataStore.ProspectiveHousing:
            self.DataStore.Logger.addToLog("Length:{0}".format(int(math.ceil((len(self.DataStore.EnvActors) + 4 - self.DataStore.ProspectiveHousing) / 5.0))), 0)
            for x in range(0, int(math.ceil((len(self.DataStore.EnvActors) + 4 - self.DataStore.ProspectiveHousing) / 5.0))):
                while True:
                    id = random.randint(0, len(self.DataStore.EnvTiles) -1)
                    if self.DataStore.EnvTiles[id].ResourceType == "None":
                        self.DataStore.EnvTiles[id].Structure = House(self.DataStore, self.DataStore.EnvTiles[id])
                        self.DataStore.addProspective(5)
                        self.DataStore.Village.addWant(VillageRequest("Build:{0}".format(id), 2), 1)
                        break

    def AnalyzeMoreVillagers(self):        
        if self.AverageHungerLimitForMore < 50 and len(self.DataStore.EnvActors) + 1 <= self.DataStore.HousingAvilable:
            if self.DataStore.Village.Resources["Food"] / self.TotalConsumption > self.StoreLimitForMore:
                self.DataStore.Village.addWant(VillageRequest("Mate", 1), 2)
            else:
                self.DataStore.Village.addWant(VillageRequest("Gather:Food", 2), 1)
        else:
            self.DataStore.Village.addWant(VillageRequest("Gather:Food", 1), 1)

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
            self.DataStore.Village.addNeed(VillageRequest("Gather:Food", 0), int(math.ceil(diffFoods / self.FoodPerWorkerNeededNeeded)))
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
