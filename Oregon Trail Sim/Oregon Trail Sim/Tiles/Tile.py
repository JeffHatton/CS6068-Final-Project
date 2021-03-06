﻿import Ids.Id
import threading

class Tile(threading.Thread):
    """description of class"""

    def __init__(self, dataStore):
        self.ID = Ids.Id.Id(False)
        self.ActorsInTile = dict()
        self.ActorLock = threading.Lock()
        self.Structure = None
        self.ResourceType = "None"
        self.GatherAmountGiven = 10
        self.GatherTime = .15
        self.Walkable = True
        self.DataStore = dataStore

    def AddActor(self, actor):
        self.ActorLock.acquire()
        self.ActorsInTile[actor.ID.GUID] = actor
        self.ActorLock.release()
        self.DataStore.addFresh(self)

    def RemoveActor(self, actor):
        self.ActorLock.acquire()
        #print(self.ActorsInTile)
        #print(self.ID.LocalId)
        del self.ActorsInTile[actor.ID.GUID]
        self.ActorLock.release()
        self.DataStore.addFresh(self)

    def GetActorCount(self):
        return len(self.ActorsInTile)