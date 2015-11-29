from threading import *
import Ids.Id
import time
import random

class Actor(Thread):
    """description of class"""
    id     

    def run(self):
        self.id = Ids.Id.Id(True)
        for x in range(10):            
            print(self.id.GUID)
            time.sleep(random.randint(1000,3000) / 1000)


