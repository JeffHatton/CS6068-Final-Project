from IdGenerator import *

class Id(object):
    """description of class"""

    def __init__(self, generateId):
        self.GUID =  IdGenerator.GenerateId() if generateId else -1
        self.IdX = -1
        self.IdY = -1
        self.LocalId = -1




