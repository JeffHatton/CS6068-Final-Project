from Villlages.Buildings.Building import *
from Actors.VilagerActor import *

class House(Building):
    """description of class"""

    def __init__(self, dataStore, tile):
        super(House, self).__init__(dataStore, tile)
        self.ResouceCost["Wood"] = 100
        self.WokersRequiredToBuild = 1;
        self.TimeToBuild = 5
        self.NumberHoused = 5
        self.BuildingType = "House"
        self.VillagersRequiredToWork = 2
        self.WorkTime = 20

    def WorkFinished(self):
        actor = VilagerActor(self.DataStore, self.DataStore.EnvTiles[len(self.DataStore.EnvTiles) / 2])
        self.DataStore.AddActor(actor)

    def BuildingFinished(self):
        self.DataStore.addHousing(self.NumberHoused)



