from threading import *
import math
import random
import Data.DataStore

class Village(object):
    """description of class"""

    def __init__(self, dataStore):
        self.Center = (-1 ,-1)
        self.ResourceLock = Lock()
        self.WantsNeedsLock = Lock()
        self.ActiveProjects = list()
        self.Resources = dict()
        self.Resources["Wood"] = 100
        self.Resources["Food"] = 0
        self.Resources["Stone"] = 0
        self.DataStore = dataStore
        self.Needs = list()
        self.Wants = list()

    def addResource(self, resourceChanges):
        self.ResourceLock.acquire()        
        for resourceType, changeValue in resourceChanges:
            self.DataStore.Logger.addToLog("{0} {1} Collected".format(changeValue, resourceType), 4)
            if resourceType not in self.Resources.keys():
                self.Resources[resourceType] = changeValue
            else:
                self.Resources[resourceType] += changeValue

        self.ResourceLock.release()

    def requestResources(self, resourceChanges):
        for resourceType, changeValue in resourceChanges.iteritems():
            self.requestResource(resourceType, changeValue)

    def requestResource(self, resourceType, amount, allOrNothing = True):
        self.ResourceLock.acquire()        
        returnAmount = 0             

        if resourceType not in self.Resources.keys():
            return returnAmount

        self.DataStore.Logger.addToLog("{0} {1} Requested".format(amount, resourceType), 3)
        if self.Resources[resourceType] >= amount:
            self.Resources[resourceType] -= amount
            returnAmount = amount
        elif allOrNothing == False:
            temp = self.Resources[resourceType]
            self.Resources[resourceType] = 0
            returnAmount = temp

        self.ResourceLock.release()    
        return returnAmount    
    
    def addNeeds(self, Needs):
        self.WantsNeedsLock.acquire()
        for need in Needs:
            self.Needs.append(need)
            self.DataStore.Logger.addToLog("Work Need Added: {0}".format(need.ActionNeeded), 2)
        self.Needs = sorted(self.Needs, key =  lambda need: need.Priority)
        self.WantsNeedsLock.release()

    def addWants(self, wants):
        self.WantsNeedsLock.acquire()
        for need in wants:
            self.Wants.append(need)
        self.Wants = sorted(self.Wants, key =  lambda need: need.Priority)
        self.WantsNeedsLock.release()

    def giveWork(self):
        self.WantsNeedsLock.acquire()
        if len(self.Needs) > 0:            
            need = self.Needs.pop(0)
            self.DataStore.Logger.addToLog("Work Need Given: {0}".format(need.ActionNeeded), 2)
            self.WantsNeedsLock.release()
            return need.ActionNeeded
        elif len(self.Wants) > 0:
            want = self.Needs.pop(0)
            self.DataStore.Logger.addToLog("Work Want Given: {0}".format(want.ActionNeeded), 2)
            self.WantsNeedsLock.release()
            return want.ActionNeeded
        else:
            # If nothing else is needed gather random
            self.WantsNeedsLock.release()
            allResources = self.DataStore.AllResources()
            return "Gather:" + allResources[random.randint(0,len(allResources) - 1)]
