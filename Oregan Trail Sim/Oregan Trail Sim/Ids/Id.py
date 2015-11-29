from IdGenerator import *

class Id(object):
    """description of class"""
    IdX = -1
    IdY = -1
    GUID = -1
    LocalId = -1

    def __init__(self, generateId):
        self.GUID =  IdGenerator.GenerateId() if generateId else -1




