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
            threadSleepTime = random.randint(500, 3000) / 1000
            if self.CurrentTask == "Gather":                    
                if self.CurrentAction == "Idle":
                    continueLoop = True
                    while continueLoop:
                        tileId = random.randint(0,99)                
                        print("Trying to move to {0} Tile Type: {1} From {2}").format(tileId, self.DataStore.EnvTiles[tileId].ResourceType, self.CurrentTile.ID.LocalId)
                        if self.DataStore.EnvTiles[tileId].Walkable:                                       
                            self.CurrentMovePath = self.determinePath(tileId)                                
                            print("Taking path {0}").format(self.CurrentMovePath)
                            self.CurrentAction = "Moving"
                            continueLoop = False
                elif self.CurrentAction == "Moving":
                    if len(self.CurrentMovePath) == 0:
                        self.CurrentAction = "Gather"
                        print("Reached Dest start gathering")
                    else:
                        movePoint = self.CurrentMovePath.pop()
                        self.MoveTo(self.DataStore.EnvTiles[movePoint])                        
                        threadSleepTime = 1 / self.MoveSpeed
                        print("Moving to {0} wating {1} s before moving again").format(movePoint, threadSleepTime)
                elif self.CurrentAction == "Gather":
                    self.GatherFromTile()
                    self.CurrentAction = "Idle"
                    self.CurrentTask = "Gather"
                    print("Gathering")

            time.sleep(threadSleepTime)

    def GatherFromTile(self):
        if self.CurrentTile.ResourceType != "None":
            self.DataStore.Village.addResource([{self.CurrentTile.ResourceType, self.CarryLimit}])

