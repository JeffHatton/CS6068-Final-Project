from Villlages.Buildings.Building import *

class StockPile(Building):
    """description of class"""

    def __init__(self, dataStore, tile):
        super(StockPile, self).__init__(dataStore, tile)
        self.ResouceCost["Wood"] = 100
        self.WokersRequiredToBuild = 2;
        self.TimeToBuild = 10
        self.BuildingType = "StockPile"