import time
import os

command_string = "python Oregon_Trail_Sim.py > myLog.log"
os.system(command_string)

log = open('myLog.log', 'r')
logString = log.read()

time1 = logString[39:52]
end = len(logString)
time2 = logString[end-14:end-1]

print(time1)
print(time2)
print(float(time2) - float(time1))
