from LivingActor import *
import random
import time

class VilagerActor(LivingActor):
    """description of class"""

    def __init__(self, dataStore, tile):
        LivingActor.__init__(self, dataStore, tile)
        self.PreferedAction = "Gather"

    def run(self):
            while True:
                tileId = random.randint(0,99)
                self.MoveTo(self.DataStore.EnvTiles[tileId])

                self.GatherFromTile()
                time.sleep(random.randint(500, 3000) / 1000)

    def GatherFromTile(self):
        if self.CurrentTile.ResourceType != "None":
            self.DataStore.Village.addResource([{self.CurrentTile.ResourceType, self.CarryLimit}])

