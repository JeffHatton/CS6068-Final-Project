from threading import *
import Ids.Id
import time
import random
import Data

class Actor(Thread):
    """description of class"""

    def __init__(self, dataStore):
        Thread.__init__(self)
        self.DataStore = dataStore
        self.ID = Ids.Id.Id(True)
        self.CurrentAction = "Idle"
        self.CurrentTask = "Idle"

    def run(self):        
        return


