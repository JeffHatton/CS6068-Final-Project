class IdGenerator(object):
    """description of class"""
    CurrentId = 0

    @staticmethod
    def GenerateId():
        id = IdGenerator.CurrentId
        IdGenerator.CurrentId += 1
        return id

