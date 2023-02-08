import sys


M = 99
from queue import PriorityQueue

class Node:
    def __init__(self, sumDif, arr, addPair, excPair):
        self.value = sumDif
        self.arr = arr
        self.addPair = addPair
        self.excPair = excPair
    def getArr(self):
        return self.arr
    def getSumDif(self):
        return self.value
    def setSumDif(self, sumDif):
        self.value = sumDif
    def __lt__(self, other):
        return self.value < other.value

def matrixCopy(arr):
    n = len(arr)
    newArr = [[0]*n for i in range(n)]
    for i in range(n):
        for j in range(n):
            newArr[i][j] = arr[i][j]
    return newArr

def clearZeroMinus(arr):
    n = len(arr)
    for i in  range(n):
        for j in range(n):
            if arr[i][j]<0:
                arr[i][j]=0

def printMatrix(arr, st):
    n = len(arr)
    #print()
    print(st)
    for i in range(n):
        for j in range(n):
            print(arr[i][j], end=" ")
        print()
    #print()

def printEdge(arr):
    n = len(arr)
    tempArr = list(arr)
    print("Ребра які включаемо до відповіді:", end=" ")
    for i in range(n):
        print(tempArr[i][0]+1, tempArr[i][1]+1, sep="-", end=", ")
    print()


def matricReduction(arr):
    print("-Редукція матриці-")
    n = len(arr)
    arrMinRow = [M]*n
    for i in range(n):
        for j in range(n):
            if arr[i][j]!=M and arr[i][j]>0:
                arrMinRow[i] = min(arrMinRow[i], arr[i][j])
            elif arr[i][j]<=0:
                arrMinRow[i]=0
                break
        if arrMinRow[i]==M:
            arrMinRow[i]=0

    for i in range(n):
        for j in range(n):
            if arr[i][j]!=M:
                arr[i][j]-=arrMinRow[i]

    #printMatrix(arr)
    print("Мінімум по строкам ",arrMinRow)
    arrMinColumn = [M]*n
    for j in range(n):
        for i in range(n):
            if arr[i][j]!=M and arr[i][j]>=0:
                arrMinColumn[j] = min(arrMinColumn[j], arr[i][j])
            elif arr[i][j]<=0:
                arrMinColumn[i]=0
                break
        if arrMinColumn[j]==M:
            arrMinColumn[j]=0

    for j in range(n):
        for i in range(n):
            if arr[i][j]!=M:
                arr[i][j]-=arrMinColumn[j]

    print("Мінімум по стовбцям ",arrMinColumn)
    #print("Редуцьована матриця")
    printMatrix(arr, "Редукція матриці")
    sumDifR = sum(arrMinRow)
    sumDifC = sum(arrMinColumn)
    sumDif = sumDifR+sumDifC
    #printMatrix(arr)
    #(sumDif)
    return arr,sumDif

def zeroChange(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n):
            minRow = M
            minCol = M
            if arr[i][j]==0:
                for k in range(n):
                    if k!=j and arr[i][k]>0 and arr[i][k]!=M:
                        minRow = min(minRow, arr[i][k])
                    elif k!=j and arr[i][k]<=0 and arr[i][k]!=M:
                        minRow =0
                        break
                for k in range(n):
                    if k!=i and arr[k][j]>0 and arr[k][j]!=M:
                        minCol = min(minCol, arr[k][j])
                    elif k!=i and arr[k][j]<=0 and arr[k][j]!=M:
                        minCol =0
                        break
                arr[i][j] = (minRow+minCol)*-1
    #print(minRow, minCol)


def findMaxZero(arr):
    n = len(arr)
    converMax = 0
    nI = 0
    nJ = 0
    for i in range(n):
        for j in range(n):
            if arr[i][j]<0 and arr[i][j]<converMax:
                converMax = arr[i][j]
                nI = i
                nJ = j
    return nI, nJ

def dontTake(arr, nI, nJ, sumDif):
    n = len(arr)
    minR = M
    minC = M
    arr[nI][nJ]=M
    clearZeroMinus(arr)
    newArr, sumPop = matricReduction(arr)
    print("+ ", sumPop, " Якщо ми не включаємо ребро ", nI+1, "-", nJ+1, sep="")
    return newArr, sumPop

def takeSug(arr, nI, nJ, sumDif):
    arr[nJ][nI]=M
    n = len(arr)
    clearZeroMinus(arr)
    for i in range(n):
        arr[i][nJ]=M
        arr[nI][i]=M
    newArr, sumPop = matricReduction(arr)
    print("+ ", sumPop, " Якщо ми включаємо ребро ", nI+1, "-", nJ+1, sep="")
    return newArr, sumPop


def TSP(arr):

    tempArr = matrixCopy(arr)
    arr2, sumDif = matricReduction(tempArr)
    mainPQ = PriorityQueue()
    mainPQ.put(Node(sumDif, arr2, [], []))
    n = len(arr)
    itr = 1
    while mainPQ.empty()==False:
        print("#######################################################")
        print("Ітерація ", itr)
        itr+=1

        currQ = mainPQ.get()
        arr2 = currQ.arr
        sumDif = currQ.getSumDif()
        #print("Ребро включення та виключення ", currQ.addPair[0], currQ.addPair[1] )
        takeEdge = list(currQ.addPair)
        dontEdge = list(currQ.excPair)

        print("нижня границя: ", currQ.getSumDif())
        #print("Ребра які включаемо до відповіді: ", takeEdge)
        printEdge(takeEdge)
        #print("don't take", currQ.excPair)
        if len(takeEdge)==len(arr)-1:
            mis1 = [0]*n
            mis2 = [0]*n
            for i in range(len(takeEdge)):
                mis1[takeEdge[i][0]]=1
                mis2[takeEdge[i][1]]=1
            l,r = 0, 0
            for i in range(n):
                if mis1[i]==0:
                    l = i
                if mis2[i]==0:
                    r= i
            print("Останнє ребро включення ", l+1,"-", r+1, sep="")
            takeEdge.append([l,r])

            print()
            print("Мінімальна вартість:",  currQ.getSumDif())
            printEdge(takeEdge)
            sys.exit(0)
        zeroChange(arr2)
        nI, nJ = findMaxZero(arr2)
        printMatrix(arr2, "Знаходження ребра включення та виключення")
        print("Ребро включення та виключення ", nI+1, "-", nJ+1, sep="")
        clearZeroMinus(arr2)
        #printMatrix(arr2)
        #print(nI, nJ, "sfdsf")
        print("Виключаємо ребро------------------------------------")
        #don't take
        arr3, newSumDif = dontTake(arr2, nI, nJ, sumDif)
        arr3 = matrixCopy(arr3)
        #printMatrix(arr3)
        dontEdge.append([nI, nJ])
        NodeDontTake = Node(sumDif+newSumDif, arr3, takeEdge, dontEdge)
        mainPQ.put(NodeDontTake)

        takeEdge = list(currQ.addPair)
        dontEdge = list(currQ.excPair)
        print("Влючаємо ребро---------------------------------------")
        #take
        arr4, newSumDif = takeSug(arr2, nI, nJ, sumDif)
        takeEdge.append([nI, nJ])
        #printMatrix(arr4)
        NodeTake = Node(sumDif+newSumDif, arr4, takeEdge, dontEdge)
        mainPQ.put(NodeTake)

if __name__ == "__main__":
    TSP([[M, 4, 5, 6, 6],
         [5, M, 4, 5, 4],
         [3, 7, M, 5, 6],
         [4, 3, 5, M, 6],
         [7, 4, 4, 5, M]])


