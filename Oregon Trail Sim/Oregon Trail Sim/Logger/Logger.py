import threading
import logging
import sys
import os

class Logger(object):
    """description of class"""
    
    def __init__(self, logLevel, outputDirectory=os.getcwd(), fileName="oregon_trail_sim.txt"):
        self.LogLevel = logLevel
        self.LogLock = threading.Lock()
        self.LogMessage = ""
        self.PrintToConsole = True

        logFormatter = logging.Formatter("%(asctime)s - %(message)s")
        self.RootLogger = logging.getLogger('')
        self.RootLogger.setLevel(logging.DEBUG)

        fileHandler = logging.FileHandler("{0}/{1}.log".format(outputDirectory, fileName))
        fileHandler.setFormatter(logFormatter)        
        self.RootLogger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(logFormatter)
        self.RootLogger.addHandler(consoleHandler)

    def addToLog(self, logMessage, logLevel):
        if logLevel <= self.LogLevel:
            self.LogLock.acquire()
            self.LogMessage += logMessage + "\n"
            if self.PrintToConsole:
                self.RootLogger.info(logMessage)
            self.LogLock.release()   