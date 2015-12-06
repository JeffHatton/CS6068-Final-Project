import threading
import time

class Logger(object):
    """description of class"""
    
    def __init__(self, logLevel):
        self.LogLevel = logLevel
        self.LogLock = threading.Lock()
        self.LogMessage = ""
        self.PrintToConsole = True

        # Handle File Output. TODO: Verify file location
        self.PrintToFile = True
        self.LogFile = open("Temp/" + time.strftime("%Y%m%d-%H%M%S") + ".txt", 'w')
       
    def addToLog(self, logMessage, logLevel):
        if logLevel <= self.LogLevel:
            self.LogLock.acquire()
            self.LogMessage += logMessage + "\n"
            if self.PrintToConsole:
                print(logMessage)
            if self.PrintToFile:
                self.LogFile.write(logMessage + "\n")
                self.LogFile.flush()
            self.LogLock.release()
         
