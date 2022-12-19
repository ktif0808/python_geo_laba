import matplotlib.pyplot as plt
import numpy as np
import mplcursors
import statistics






class Algorithm_LB3:
    @staticmethod
    def convertDataStepAver(dpPrefSum, arrCheckPoint, startTime, step):
        if step<=0:
            raise Exception("step must be bigger than 0")
        valuePointStep = []
        countPointStep = 0
        timePointStep = []
        for i in range(1, len(dpPrefSum)):
            if arrCheckPoint[i]==1:
                countPointStep+=1
            if i%step==0:
                temp = (dpPrefSum[i]-dpPrefSum[i-step])/countPointStep
                countPointStep = 0
                valuePointStep.append(temp)
                timePointStep.append(i+startTime)
        return [timePointStep, valuePointStep]

    @staticmethod
    def roundValue(value, afterDot):
        return np.around([float(value)], decimals=afterDot, out=None)[0]




class DrawPlot:

    @staticmethod
    def buildPlot2D(xData, yData, aver, maxDif, title):
        maxDif = Algorithm_LB3.roundValue(maxDif, 3)
        aver[0] = Algorithm_LB3.roundValue(aver[0], 3)
        def textRun(annotation):
            syt = annotation.replace('x', "seconds")
            syt = syt.replace('y', "degree")
            dd = list(map(str, syt.split('=')))
            valueCon = None
            try:
                valueCon = float(dd[len(dd)-1])
            except ValueError:
                valueCon = float(dd[len(dd)-1][1:])*(-1)
            diff = abs(aver[0]-valueCon)
            diff = Algorithm_LB3.roundValue(diff, 8)
            syt = syt+"\n deviation "+str(diff)
            return syt
        plt.style.use('seaborn-whitegrid')
        fig, ax = plt.subplots()
        fig.set(facecolor = 'lightblue')
        ax.plot(xData, yData, color="blue")
        ax.plot(xData, aver[:len(yData)], color='red')
        ax.set_xlabel("seconds", fontsize=20)
        ax.set_ylabel("degree", fontsize=20)
        plt.title(title +" average value: "+str(aver[0]), fontsize=20)
        dots = ax.scatter(xData, yData, color='darkred')
        crs = mplcursors.cursor(dots, hover=True)
        crs.connect("add", lambda sel: sel.annotation.set_text(textRun(sel.annotation.get_text())))
        for x,y in zip(xData, yData):
            curPoint = Algorithm_LB3.roundValue(float(abs(float(y)-aver[0])), 3) #np.around([float(abs(y-aver[0]))], decimals=3, out=None)[0]
            if curPoint==maxDif:
                ax.scatter(x, y, color='red')
        plt.legend(['dependency', 'Average', 'checkpoint', 'maxDif'], loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=12, frameon=True)
        plt.show()





class PlotBuilder:

    def __init__(self, arrData, type):
        self._arrData = arrData
        self.executeData(self._arrData, type)


    def executeData(self, arrData, type):

        startTime = int(arrData[0][6][:-4])-1
        endTime = int(arrData[len(arrData)-1][6][:-4])
        column = None
        if type=="head":
            column = 12
        else:
            column = 13
        arrtimeX = []
        arrDegree = []
        dpPrefSum = [0]*((endTime-startTime)+1)
        arrCheckPoint = [0]*((endTime-startTime)+1)
        for i in range(0, len(arrData)):
            strD = int(arrData[i][6][:-4])
            arrtimeX.append(strD)
            arrDegree.append(Algorithm_LB3.roundValue(self._arrData[i][column],8))
            dpPrefSum[strD-startTime]=Algorithm_LB3.roundValue(self._arrData[i][column],8)
            arrCheckPoint[strD-startTime] = 1

        averData = sum(dpPrefSum)/len(arrData)
        maxDifL = Algorithm_LB3.roundValue(max(list(map(lambda x: x!=0 and abs(averData-x), dpPrefSum))),3)

        for i in range(1, len(dpPrefSum)):
            dpPrefSum[i] = Algorithm_LB3.roundValue(dpPrefSum[i]+dpPrefSum[i-1],8)

        arrAver = [averData]*len(arrData)
        arrAver = np.array(arrAver)
        arrAver = arrAver.astype(np.float64)
        arrDegree = np.array(arrDegree)
        arrDegree = arrDegree.astype(np.float64)
        arrtimeX = np.array(arrtimeX)
        arrtimeX = arrtimeX.astype(np.float64)


        self._arrDegree = arrDegree
        self._arrtimeX = arrtimeX
        self._arrAver = arrAver
        self._maxDif = maxDifL
        self._averData = averData
        self._startTime = startTime
        self._dpTime = dpPrefSum
        self._arrCheckPoint = arrCheckPoint
        self._type = type




    def plotData(self):
        DrawPlot.buildPlot2D(self._arrtimeX, self._arrDegree, self._arrAver, self._maxDif, 'Dependency time - degree ' + self._type+', second, ')

    def printData(self):
        for i in range(len(self._arrData)):
            print(i+1, int(self._arrData))

    def getAverageValue(self):
        return Algorithm_LB3.roundValue(self._averData, 8)

    def getMaxAverDiff(self):
        return Algorithm_LB3.roundValue(self._maxDif, 8)

    def getStatictic(self):
        return Algorithm_LB3.roundValue(statistics.stdev(self._arrDegree), 8)





class PlotBuilderStep(PlotBuilder):
    def __init__(self, arrData, type, step):
        #super(arrData)
        self._arrData = arrData
        self.executeData(self._arrData, type)
        self._arrTimeStep, self._arrStepDegree = Algorithm_LB3.convertDataStepAver(self._dpTime, self._arrCheckPoint, self._startTime, step)
        self._averData = sum(self._arrStepDegree)/len(self._arrStepDegree)
        maxDifStepL = Algorithm_LB3.roundValue(max(list(map(lambda x: abs(self._averData-x), self._arrStepDegree))),3)
        averData = sum(self._arrStepDegree)/len(self._arrStepDegree)
        arrAverStep = [averData] * len(self._arrStepDegree)
        self._maxDifStep = maxDifStepL
        self._arrAverStep = arrAverStep
        self._averData = averData
        self._step = step

    def getAverageValue(self):
        return Algorithm_LB3.roundValue(self._averData, 8)
    def getMaxAverDiff(self):
        return Algorithm_LB3.roundValue(self._maxDifStep, 8)
    def plotData(self):
        DrawPlot.buildPlot2D(self._arrTimeStep, self._arrStepDegree, self._arrAverStep, self._maxDifStep,  'Dependency time - degree ' + self._type+' and seconds, interval '+str(self._step)+' s, ')
    def getStatictic(self):
        return Algorithm_LB3.roundValue(statistics.stdev(self._arrStepDegree), 8)




def readFile(pathFile):
    file1 = open(pathFile, 'r')
    Lines = file1.readlines()
    arrData = []
    for line in Lines:
        st = list(map(str, line.split(',')))
        arrData.append(st)
    return arrData


if __name__ == "__main__":

    dataFlight = readFile('\\python_laba\\resourse\\cvGPS.csv')
    plotBuilderH = PlotBuilder(dataFlight, "head")
    plotBuilderP = PlotBuilder(dataFlight, "pitch")
    plotBuilder10H = PlotBuilderStep(dataFlight, "head", 10)
    plotBuilder10P = PlotBuilderStep(dataFlight, "pitch", 10)
    plotBuilder20H = PlotBuilderStep(dataFlight, "head", 20)
    plotBuilder20P = PlotBuilderStep(dataFlight, "pitch", 20)

    plotBuilderH.plotData()
    plotBuilderP.plotData()
    plotBuilder10H.plotData()
    plotBuilder10P.plotData()
    plotBuilder20H.plotData()
    plotBuilder20P.plotData()

    print("calculation")
    print("середнє значення (head):", plotBuilderH.getAverageValue())
    print("максимальне відхилення від середнього значення (head):", plotBuilderH.getMaxAverDiff())
    print("середньо квадратичне відхилення (head):", plotBuilderH.getStatictic())
    print("середнє значення (pitch):", plotBuilderP.getAverageValue())
    print("максимальне відхилення від середнього значення(pitch):", plotBuilderP.getMaxAverDiff())
    print("середньо квадратичне відхилення (head):", plotBuilderP.getStatictic())
    print("середнє значення з кроком кутів 10c (head):", plotBuilder10H.getAverageValue())
    print("максимальне відхилення від середнього значення з кроком кутів 10c (head):", plotBuilder10H.getMaxAverDiff())
    print("середньо квадратичне відхилення з кроком кутів 10c (head):", plotBuilder10H.getStatictic())
    print("середнє значення з кроком кутів 10c (pitch):",plotBuilder10P.getAverageValue())
    print("максимальне відхилення від середнього значення з кроком кутів 10c (pitch):", plotBuilder10P.getMaxAverDiff())
    print("середньо квадратичне відхилення з кроком кутів 10c (pitch):",plotBuilder10P.getStatictic())
    print("середнє значення з кроком кутів 20c (head):", plotBuilder20H.getAverageValue())
    print("максимальне відхилення від середнього значення з кроком кутів 20c (head):", plotBuilder20H.getMaxAverDiff())
    print("середньо квадратичне відхилення з кроком кутівstandard deviation 20c (head):", plotBuilder20H.getStatictic())
    print("середнє значення з кроком кутів 20c (pitch):", plotBuilder20P.getAverageValue())
    print("максимальне відхилення від середнього значення з кроком кутів 20c (pitch):", plotBuilder20P.getMaxAverDiff())
    print("середньо квадратичне відхилення з кроком кутів 20c (pitch):", plotBuilder20P.getStatictic())

