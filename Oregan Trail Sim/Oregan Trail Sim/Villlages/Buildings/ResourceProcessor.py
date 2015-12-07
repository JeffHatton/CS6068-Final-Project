from Villlages.Buildings.Building import *

class ResourceProcessor(Building):
    """description of class"""

    def __init__(self, dataStore, tile, inputResource, outputResource, inAmount, outAmount):
        super(ResourceProcessor, self).__init__(dataStore, tile)

        self.BuildingType = "ResourceProcessor"
        self.WorkTime = 10
        self.WokersRequiredToBuild = 3
        self.VillagersRequiredToWork = 1
        self.TimeToBuild = 10
        self.InputResource = inputResource
        self.OutputResource = outputResource        
        self.WorkResourceCost[inputResource] = inAmount
        self.WorkResourceProduce[self.OutputResource] = outAmount


class FoodProcessor(ResourceProcessor):
    """description of class"""

    def __init__(self, dataStore, tile):
        super(FoodProcessor, self).__init__(dataStore, tile, "Food", "Food", 10, 250)
        self.WorkTime = 5
        self.TimeToBuild = 5
        self.BuildingType = "FoodProcessor"
        self.ResouceCost["Wood"] = 200
        self.ResouceCost["Iron"] = 100
        self.ResouceCost["Stone"] = 100

class StoneProcessor(ResourceProcessor):
    """description of class"""

    def __init__(self, dataStore, tile):
        super(StoneProcessor, self).__init__(dataStore, tile, "Stone", "PStone", 10, 10)
        self.WorkTime = 30
        self.ResouceCost["Wood"] = 200
        self.ResouceCost["Iron"] = 100

class IronProcessor(ResourceProcessor):
    """description of class"""

    def __init__(self, dataStore, tile):
        super(IronProcessor, self).__init__(dataStore, tile, "Iron", "PIron", 10, 10)
        self.WorkTime = 20

        self.ResouceCost["Wood"] = 200
        self.ResouceCost["Iron"] = 100
        self.ResouceCost["Pstone"] = 100