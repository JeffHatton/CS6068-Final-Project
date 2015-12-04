from threading import *
import math
class Village(object):
    """description of class"""

    def __init__(self):
        self.Center = (-1 ,-1)
        self.ResourceLock = Lock()
        self.ActiveProjects = list()
        self.Resources = dict()
        self.Resources["Wood"] = 0
        self.Resources["Food"] = 0
        self.Resources["Stone"] = 0

    def addResource(self, resourceChanges):
        self.ResourceLock.acquire()        
        for resourceType, changeValue in resourceChanges:
            print("{0} {1} Collected").format(changeValue, resourceType)
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

        print("{0} {1} Requested").format(amount, resourceType)
        if self.Resources[resourceType] >= amount:
            self.Resources[resourceType] -= amount
            returnAmount = amount
        elif allOrNothing == False:
            temp = self.Resources[resourceType]
            self.Resources[resourceType] = 0
            returnAmount = temp

        self.ResourceLock.release()    
        return returnAmount    
