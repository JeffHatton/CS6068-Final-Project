from IdConverter import *

class DataStore(object):
    """Global Storage for Application"""

    #Dictionary of Actors Key:ID Value: Actor
    Actors = dict()
    Tiles = dict()
    EnvironmentDimX
    EnvironmentDimY
    TileIdConverter

    def AddActor(actor):
        print("Implement Add Actor")

    def RemoveActor(id):
        print("Implement remove actor")
    
    def MorpthActor(id, newActorType):
        print("Implement morpth actor")

    def AddTile(tile):
        print("Implement Add Tile")

    def RemoveTile(id):
        print("Implement remove Tile")
    
    def MorpthTile(id, newTileType):
        print("Implement morpth Tile")

    def SetEnvironmentDim(self, x, y):
        self.TileIdConverter = IdConverter(x, y, True)
        self.EnvironmentDimX = x
        self.EnvironmentDimY = y