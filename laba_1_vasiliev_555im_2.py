import matplotlib.pyplot as plt
import numpy as np
import mplcursors
import matplotlib.dates as mdates
from datetime import datetime
from geopy import distance
from pyproj import Geod
from geographiclib.geodesic import Geodesic
import sys



class DistanceCalculator:

    #I will use this method for all my examples as a default
    @staticmethod
    def getDistanceGeopy(point1, point2):
        distance_2d= distance.distance(point1[:2], point2[:2]).m
        distance_3d = np.sqrt(distance_2d**2 + (point1[2] - point2[2])**2)
        return np.around([distance_3d], decimals=2, out=None)[0]

    @staticmethod
    def getDistanceGeod(point1, point2):
        g = Geod(ellps='WGS84')
        azimuth1, azimuth2, distance_2d = g.inv(point1[1], point1[0], point2[1], point2[0])
        distance_3d = np.hypot(distance_2d,point2[2]-point1[2])
        return np.around([distance_3d], decimals=2, out=None)[0]

    @staticmethod
    def getDistanceGeodesic(point1, point2):
        geod = Geodesic.WGS84
        g = geod.Inverse(point1[0], point1[1],point2[0],point2[1])
        distance_3d = np.hypot(g['s12'],point2[2]-point1[2])
        return np.around([distance_3d], decimals=2, out=None)[0]

#sys.exit(0)

class DrawPlot:

    @staticmethod
    def buildPlot2D(xData, yData, xlabel, ylabel, title, colorPlot):
        def textRun(annotation):
            syt = annotation.replace('x', xlabel)
            syt = syt.replace('y', ylabel)
            return syt
        plt.style.use('seaborn-whitegrid')
        myFmt = mdates.DateFormatter('%H:%M:%S')
        fig, ax = plt.subplots()

        faceColor = None
        pointColor = None
        if colorPlot == "blue":
            faceColor = 'lightblue'
            pointColor = 'darkred'
        elif colorPlot == "darkgreen":
            faceColor = 'antiquewhite'
            pointColor = 'red'
        elif colorPlot == 'darkorange':
            faceColor = 'lavender'
            pointColor = 'darkred'
        else:
            raise Exception("Incorect input")

        fig.set(facecolor = faceColor)
        ax.plot(xData, yData, color=colorPlot)
        ax.set_xlabel(xlabel, fontsize=20)
        ax.set_ylabel(ylabel, fontsize=20)
        plt.title(title, fontsize=20)
        dots = ax.scatter(xData, yData, color=pointColor)
        plt.legend(['dependency', 'checkpoint'], loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=12, frameon=True)
        ax.xaxis.set_major_formatter(myFmt)
        crs = mplcursors.cursor(dots, hover=True)
        crs.connect("add", lambda sel: sel.annotation.set_text(textRun(sel.annotation.get_text())))
        plt.show()

    @staticmethod
    def drawPlot(plan, dependency):
        if dependency=="time-speed":
            DrawPlot.buildPlot2D(plan._timeHigh, plan._arrSpeed, 'check time (control point)', \
                                 'speed (m/s)', 'The plot of dependency of speed to time', 'blue')
        elif dependency=="time-altitude":
            DrawPlot.buildPlot2D(plan._timeHigh, plan._arrHight, 'check time (control point)', \
                                 'altitude (m)', 'The plot of dependency of altitude to time', 'darkgreen')
        elif dependency=="time-distance":
            DrawPlot.buildPlot2D(plan._timeHigh, plan._arrDis, 'check time (control point)', \
                                 'distance (m)', 'The plot of dependency of distance to time', 'darkorange')
        else:
            raise Exception("Incorect input")


class Airplane:

    def __init__(self, arrData, distanceMethod="Geopy"):
        self._arrData = arrData
        self.executeFlight(self._arrData, distanceMethod)

    def executeFlight(self, arrData, distanceMethod="Geopy"):

        sumDis = 0
        maxSpeed = 0
        minSpeed = 99999999
        minFlight = float(arrData[0][9])
        maxFlight = float(arrData[0][9])
        arrDis = [0]
        arrSpeed = [0]
        arrHight = [arrData[0][9]]


        for i in range(1, len(arrData)):
            point1 = [float(arrData[i-1][2])/100, float(arrData[i-1][4])/100, float(arrData[i-1][9])]
            point2 = [float(arrData[i][2])/100, float(arrData[i][4])/100, float(arrData[i][9])]
            dis2point = None
            if distanceMethod=="Geopy":
                dis2point = DistanceCalculator.getDistanceGeopy(point1,point2)
            elif distanceMethod=="Geod":
                dis2point = DistanceCalculator.getDistanceGeod(point1,point2)
            elif distanceMethod=="Geodesic":
                dis2point = DistanceCalculator.getDistanceGeodesic(point1,point2)
            else:
                raise Exception("Incorect input")
            sumDis+=dis2point
            arrDis.append(sumDis)
            arrSpeed.append(float(dis2point))
            arrHight.append(float(arrData[i][9]))
            maxSpeed = max(dis2point, maxSpeed)
            minSpeed = min(dis2point, minSpeed)
            minFlight = min(float(arrData[i][9]), minFlight)
            maxFlight = max(float(arrData[i][9]), maxFlight)

        #convert to numpy array
        arrSpeed = np.array(arrSpeed)
        arrSpeed = arrSpeed.astype(np.float64)
        arrHight = np.array(arrHight)
        arrHight = arrHight.astype(np.float64)
        arrDis = np.array(arrDis)
        arrDis = arrDis.astype(np.float64)


        #time plotting
        timeHigh = []
        for i in range(0, len(arrData)):
            strD = arrData[i][1][:-3]
            datetime_object = datetime.strptime(strD, '%H%M%S')
            timeHigh.append(datetime_object)
        #total seconds
        resultTime = timeHigh[len(timeHigh)-1] - timeHigh[0]



        #data request
        self._maxSpeed = maxSpeed
        self._minSpeed = minSpeed
        self._minFlight = minFlight
        self._maxFlight = maxFlight
        self._sumDis = sumDis
        self._averSpeed =sumDis/(len(arrDis)-1)
        self._timeFlight = resultTime.total_seconds()

        #array for plotting
        self._timeHigh = timeHigh
        self._arrSpeed = arrSpeed
        self._arrHight = arrHight
        self._arrDis = arrDis

    def convertMCtoKG(self, value):
        value = value/1000*3600
        return value


    #get requered paraments to our PZ
    def getMinAltitude(self):
        return np.around([self._minFlight], decimals=2, out=None)[0]
    def getMaxAltitude(self):
        return np.around([self._maxFlight], decimals=2, out=None)[0]
    def getTotalDistance(self):
        return np.around([self._sumDis], decimals=2, out=None)[0]
    def getTimeFlight(self):
        return np.around([self._timeFlight], decimals=2, out=None)[0]
    def getAverSpeed(self, convert=False):
        if convert==False:
            return np.around([self._averSpeed], decimals=2, out=None)[0]
        else:
            return np.around([self.convertMCtoKG(self._averSpeed)], decimals=2, out=None)[0]
    def getMaxSpeed(self, convert=False):
        if convert==False:
            return np.around([self._maxSpeed], decimals=2, out=None)[0]
        else:
            return np.around([self.convertMCtoKG(self._maxSpeed)], decimals=2, out=None)[0]
    def getMinSpeed(self, convert=False):
        if convert==False:
            return np.around([self._minSpeed], decimals=2, out=None)[0]
        else:
            return np.around([self.convertMCtoKG(self._minSpeed)], decimals=2, out=None)[0]


    def buildDepenency(self, dependency):
        DrawPlot.drawPlot(self, dependency)

    def setData(self, arrData, distanceMethod="Geopy"):
        self._arrData = arrData
        self.executeFlight(self._arrData, distanceMethod)
    def getData(self):
        return self._arrData
    def printData(self):
        for i in range(len(self._arrData)):
            print(i+1, self._arrData[i])



def readFile(pathFile):
    file1 = open(pathFile, 'r')
    Lines = file1.readlines()
    arrData = []
    for line in Lines:
        st = list(map(str, line.split(',')))
        arrData.append(st)
    return arrData


if __name__ == "__main__":
    dataFlight = readFile('\\python_laba\\resourse\\data.csv')
    airplane1 = Airplane(dataFlight)
    #plan1.printData()
    print("The distance that the airplane has flight:", airplane1.getTotalDistance(), "m")

    print("Maximum speed of the airplane:", airplane1.getMaxSpeed(),"m/c")
    print("Maximum speed of the airplane:", airplane1.getMaxSpeed(convert=True), "km/h")
    print("Minimum speed of the airplane:", airplane1.getMinSpeed(),"m/c")
    print("Minimum speed of the airplane:", airplane1.getMinSpeed(convert=True), "km/h")
    print("Average speed of the airplane:", airplane1.getAverSpeed(),"m/c")
    print("Average speed of the airplane:", airplane1.getAverSpeed(convert=True), "km/h")

    print("Maximum altitude of the airplane:", airplane1.getMaxAltitude(), "m")
    print("Minimum altitude of the airplane:", airplane1.getMinAltitude(), "m")
    print("Total time of the flight:", airplane1.getTimeFlight(), "s")

    airplane1.buildDepenency(dependency="time-altitude")
    airplane1.buildDepenency(dependency="time-speed")
    airplane1.buildDepenency(dependency="time-distance")
