import threading

class Logger(object):
    """description of class"""
    
    def __init__(self, logLevel):
        self.LogLevel = logLevel
        self.LogLock = threading.Lock()
        self.LogMessage = ""
        self.PrintToConsole = True

    def addToLog(self, logMessage, logLevel):
        if logLevel <= self.LogLevel:
            self.LogLock.acquire()
            self.LogMessage += logMessage + "\n"
            if self.PrintToConsole:
                print(logMessage)
            self.LogLock.release()
         
