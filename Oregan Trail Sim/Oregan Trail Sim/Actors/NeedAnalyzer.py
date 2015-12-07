from Actor import *
from Villlages.VillageRequest import *
import math
import time

class NeedAnalyzer(Actor):
    """description of class"""

    def __init__(self, dataStore):
        self.DataStore = dataStore
        self.FoodStockPilePreference = 1.25
        self.FoodPerWorkerNeededNeeded = 20
        Actor.__init__(self, dataStore)

    def run(self):
        while not self.stop_requested:
            self.AnalyzeFood()
            time.sleep(10)            

    def AnalyzeFood(self):

        if len(self.DataStore.EnvActors) == 0:
            return

        averageHunger = 0
        averageFoodHunger = 0
        totalFoodNeeded = 0
        for key,actor in self.DataStore.EnvActors.iteritems():
            averageHunger += actor.Hunger
            totalFoodNeeded += actor.Hunger / actor.FoodToHungerConversion
            averageFoodHunger += actor.FoodToHungerConversion
        
        diffFoods = (self.FoodStockPilePreference * totalFoodNeeded) - self.DataStore.Village.Resources["Food"] 
        if diffFoods > 0:
            needsList = list()
            for x in range(0, int(math.ceil(diffFoods / self.FoodPerWorkerNeededNeeded))):
                needsList.append(VillageRequest("Gather:Food", 0))
            self.DataStore.Village.addNeeds(needsList)
        averageHunger = averageHunger / len(self.DataStore.EnvActors)
