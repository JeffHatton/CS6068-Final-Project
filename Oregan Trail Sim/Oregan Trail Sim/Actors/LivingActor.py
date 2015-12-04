from Actor import *
from Data.DataStore import *

class LivingActor(Actor):
    """description of class"""
    
    def __init__(self, dataStore, tile):
        Actor.__init__(self, dataStore)
        self.CurrentTile = tile
        self.CurrentTile.AddActor(self)
        self.HP = 0
        self.CarryLimit = 5

        # How hungry the actor is
        self.Hunger = 100

        # How quickly actor gets hungry hunger/s
        self.HungerDisRate = 1

        # Tiles/s
        self.MoveSpeed = 10
        
        self.CurrentMovePath = list()

    def MoveTo(self, Tile):
        self.CurrentTile.RemoveActor(self)
        self.CurrentTile = Tile
        Tile.AddActor(self)

    def determinePath(self, tileId):
        (desX, desY) = self.DataStore.TileIdConverter.Convert1dTo2d(tileId)
        (curX, curY) = self.DataStore.TileIdConverter.Convert1dTo2d(self.CurrentTile.ID.LocalId)
        
        path = list()

        while curX != desX or curY != desY:            
            if curX < desX:
                if self.DataStore.EnvTiles[self.DataStore.TileIdConverter.Convert2dTo1d(curX + 1, curY)].Walkable:
                    curX = curX + 1
            elif curX > desX:
                if self.DataStore.EnvTiles[self.DataStore.TileIdConverter.Convert2dTo1d(curX - 1, curY)].Walkable:
                    curX = curX - 1

            if curY < desY:
                if self.DataStore.EnvTiles[self.DataStore.TileIdConverter.Convert2dTo1d(curX, curY + 1)].Walkable:
                    curY = curY + 1
            elif curY > desY:
                if self.DataStore.EnvTiles[self.DataStore.TileIdConverter.Convert2dTo1d(curX, curY - 1)].Walkable:
                    curY = curY - 1           

            path.append(self.DataStore.TileIdConverter.Convert2dTo1d(curX,curY))
            print("Adding {0} to path").format(self.DataStore.TileIdConverter.Convert2dTo1d(curX,curY))
        return path

    



