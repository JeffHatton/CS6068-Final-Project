from threading import *

class Village(object):
    """description of class"""

    def __init__(self):
        self.Center = (-1 ,-1)
        self.Food = 0
        self.Wood = 0
        self.Stone = 0
        self.ResourceLock = Lock()
        self.ActiveProjects = list()

    def addResource(self, resourceChanges):
        self.ResourceLock.acquire()        
        for resourceType, changeValue in resourceChanges:
            print("{0} {1} Collected").format(changeValue, resourceType)

            if resourceType == "Wood":                
                self.Wood = self.Wood + changeValue
            elif resourceType == "Stone":
                self.Stone = self.Stone + changeValue
            elif resourceType == "Food":
                self.Food = self.Food + changeValue

        self.ResourceLock.release()

        
