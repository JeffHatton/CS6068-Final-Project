from threading import *
import math
class Village(object):
    """description of class"""

    def __init__(self, dataStore):
        self.Center = (-1 ,-1)
        self.ResourceLock = Lock()
        self.ActiveProjects = list()
        self.Resources = dict()
        self.Resources["Wood"] = 0
        self.Resources["Food"] = 0
        self.Resources["Stone"] = 0
        self.DataStore = dataStore

    def addResource(self, resourceChanges):
        self.ResourceLock.acquire()        
        for resourceType, changeValue in resourceChanges:
            self.DataStore.Logger.addToLog("{0} {1} Collected".format(changeValue, resourceType), 3)
            if resourceType not in self.Resources.keys():
                self.Resources[resourceType] = changeValue
            else:
                self.Resources[resourceType] += changeValue

        self.ResourceLock.release()

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
