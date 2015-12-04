﻿import Ids.IdConverter
import threading
import Villlages.Village

from Tiles.TileGenerator import *
from Actors.VilagerActor import *

class DataStore(object):
    """Global Storage for Application"""

    def __init__(self, x, y, numVilagers):
        self.EnvActors = dict()
        self.EnvTiles = dict()
        self.SetEnvironmentDim(x, y)
        self.ActorLock = threading.Lock()
        self.EnvLock = threading.Lock()
        self.Village = Villlages.Village.Village()              
        for tile in TileGenerator.generateTileGrid(x, y):
            tile.ID.LocalId = self.TileIdConverter.Convert2dTo1d(tile.ID.IdX,tile.ID.IdY)
            self.AddTile(tile)

        for x in range(numVilagers):
            actor = VilagerActor(self, self.EnvTiles[x /2 + y/2])
            #actor.CurrentTask = "Gather"
            self.AddActor(actor)

    def AddActor(self, actor):
        self.ActorLock.acquire()
        self.EnvActors[actor.ID.GUID] = actor
        self.ActorLock.release()

    def RemoveActor(self, id):
        print("Implement remove actor")
    
    def MorpthActor(self, id, newActorType):
        print("Implement morpth actor")

    def AddTile(self, tile):
        self.EnvLock.acquire()
        self.EnvTiles[tile.ID.LocalId] = tile
        self.EnvLock.release()

    def RemoveTile(self, id):
        print("Implement remove Tile")
    
    def MorpthTile(self, id, newTileType):
        print("Implement morpth Tile")

    def SetEnvironmentDim(self, x, y):
        self.TileIdConverter = Ids.IdConverter.IdConverter(x, y, True)
        self.EnvironmentDimX = x
        self.EnvironmentDimY = y

    def StartSim(self):
        for key,actor in self.EnvActors.iteritems():
            actor.start()