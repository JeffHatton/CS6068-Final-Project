from Actor import *

class LivingActor(Actor):
    """description of class"""
    
    def __init__(self, dataStore, tile):
        Actor.__init__(self, dataStore)
        self.CurrentTile = tile
        self.CurrentTile.AddActor(self)
        self.HP = 0
        self.CarryLimit = 5

    def MoveTo(self, Tile):
        self.CurrentTile.RemoveActor(self)
        self.CurrentTile = Tile
        Tile.AddActor(self)


