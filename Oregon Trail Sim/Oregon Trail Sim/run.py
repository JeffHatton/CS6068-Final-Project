import time
import os

command_string = "python Oregon_Trail_Sim.py > myLog.log"

csv = open('myCSV.csv', 'w')
#csv.write("#Homes,Start,End,Total\n")
csv.write("#Homes,Run1,Run2,Run3\n")

for i in range(5, 50):
  xml = open('init.xml', 'w')
  xml.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
  xml.write("<Village width=\"20\" height=\"20\" villagers=\"" + str(i) + "\">\n")
  xml.write("\t<TileGenerator>629426204605553448</TileGenerator>\n")
  xml.write("\t<NumberOfHouses>" + str(40) + "</NumberOfHouses>\n")
  xml.write("</Village>\n")
  xml.close()

  csv.write(str(i))
  for j in range(0, 3):
    os.system(command_string)

    log = open('myLog.log', 'r')
    logString = log.read()

    time1 = logString[39:52]
    end = len(logString)
    time2 = logString[end-14:end-1]

    print(time1)
    print(time2)
    print(float(time2) - float(time1))

    csv.write(',' + str(float(time2)-float(time1)))
  csv.write("\n")
