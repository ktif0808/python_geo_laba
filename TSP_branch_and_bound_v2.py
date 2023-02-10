
#Алгоритм має багато кроків

import sys

from queue import PriorityQueue

#Після знаходження ребра розголудження ми створює 2 вузла (кейса) де ми включаємо дане ребро та виключаемо,
# та зберігаємо значення нижньої границі і  стан матриці у вузлі, оголушуємо метод порівняння def __lt__(self, other) для зберігання
# вузла у такій структурі даних як PriorityQueue
class Node:
    def __init__(self, sumDif, matrix, addPair):
        self.sumDif = sumDif
        self.matrix = matrix
        self.addPair = addPair
    def getSumDif(self):
        return self.sumDif
    def __lt__(self, other):
        return self.sumDif < other.sumDif

#Функції для здійснення побітового копіювання матриці
def matrixCopy(matrix):
    n = len(matrix)
    newArr = [[0]*n for i in range(n)]
    for i in range(n):
        for j in range(n):
            newArr[i][j] = matrix[i][j]
    return newArr

#Функції для перетворення мінусових значень в нулі
def clearZeroMinus(matrix):
    n = len(matrix)
    for i in  range(n):
        for j in range(n):
            if matrix[i][j]<0:
                matrix[i][j]=0

#Відображення стану матриці у консоль
def printMatrix(matrix, st):
    n = len(matrix)
    print(st)
    for i in range(n):
        for j in range(n):
            print(matrix[i][j], end=" ")
        print()

#Відображення ребер включення у консоль, з урахуванням, що в програмі нумерація ребер починається з 0
def printEdge(arr):
    n = len(arr)
    tempArr = list(arr)
    print("Ребра які включаемо до відповіді:", end=" ")
    for i in range(n):
        print(tempArr[i][0]+1, tempArr[i][1]+1, sep="-", end=", ")
    print()

#Функція проведення редукція матриці (зменшення всіх значень відносно максимуму по строкам та столбцям) для отримання нульових клітинок
def matricReduction(matrix):
    print("-Редукція матриці-")
    n = len(matrix)
    M = 99
    arrMinRow = [M]*n
    #Спочатку проводиться редукція по строкам, зберігаем мінімальний елемент від усіх стовбців для кожної строки
    for i in range(n):
        for j in range(n):
            if matrix[i][j]!=M and matrix[i][j]>0:
                arrMinRow[i] = min(arrMinRow[i], matrix[i][j])
            elif matrix[i][j]<=0:
                arrMinRow[i]=0
                break
        if arrMinRow[i]==M:
            arrMinRow[i]=0
    for i in range(n):
        for j in range(n):
            if matrix[i][j]!=M:
                matrix[i][j]-=arrMinRow[i]

    print("Мінімум по строкам ",arrMinRow)
    arrMinColumn = [M]*n

    #Після закінчення редукції по строкам та перетворення матриці обчислення, проводиться редукція по стовбцям.
    #зберігаем мінімальний елемент від усіх строк для кожного стовбця.
    for j in range(n):
        for i in range(n):
            if matrix[i][j]!=M and matrix[i][j]>=0:
                arrMinColumn[j] = min(arrMinColumn[j], matrix[i][j])
            elif matrix[i][j]<=0:
                arrMinColumn[i]=0
                break
        if arrMinColumn[j]==M:
            arrMinColumn[j]=0
    for j in range(n):
        for i in range(n):
            if matrix[i][j]!=M:
                matrix[i][j]-=arrMinColumn[j]

    print("Мінімум по стовбцям ",arrMinColumn)
    printMatrix(matrix, "Редукція матриці")

    #Отримаємо константу (мінімальна межа), сумму мінімумів усіх строк та стовбців з урахуванням редукції.
    sumDifR = sum(arrMinRow)
    sumDifC = sum(arrMinColumn)
    sumDif = sumDifR+sumDifC

    #Повертаємо редуцьовану матрицю та сумму константи яка вказує на те що при даній матриці відстані неможливо побудувати
    #маршрут дешевший за значення цієї константу, тотбо мінімальної межи
    return matrix,sumDif

#Функція для перетворення нулів на значення сумму(мінімального значення по стовцю + мінімального значення по рядку), де знаходиться "0" крім самого нуля
#Робимо розрахунок на скільки значення константи (мінімальної межи) буде збільшено якщо виключити ребро з нульовим значенням після редукції матриці
#Мінус ставиться для того, щоб ми могли ці клітинки матриці (нульові клітинки) відрізнити від не нульових
def zeroChange(matrix):
    M = 99
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            minRow = M
            minCol = M
            if matrix[i][j]==0:
                for k in range(n):
                    if k!=j and matrix[i][k]>0 and matrix[i][k]!=M:
                        minRow = min(minRow, matrix[i][k])
                    elif k!=j and matrix[i][k]<=0 and matrix[i][k]!=M:
                        minRow =0
                        break
                for k in range(n):
                    if k!=i and matrix[k][j]>0 and matrix[k][j]!=M:
                        minCol = min(minCol, matrix[k][j])
                    elif k!=i and matrix[k][j]<=0 and matrix[k][j]!=M:
                        minCol =0
                        break
                matrix[i][j] = (minRow+minCol)*-1

#знаходимо найменшу мінісову клітинку (найбільше значення при виключенні даного ребра розголудження)
#!!!тобто якщо ми не беремо дане ребро, то сума цільової функції збільшиться (як мінімум) на найбільше мінісове значення
def findMaxZero(matrix):
    n = len(matrix)
    converMax = 0
    nI = 0
    nJ = 0
    for i in range(n):
        for j in range(n):
            if matrix[i][j]<0 and matrix[i][j]<converMax:
                converMax = matrix[i][j]
                nI = i
                nJ = j
    return nI, nJ

#функція набору дії у тому разі якщо ми будемо виключати ребро розголудження
def fdontTakeEdge(matrix, nI, nJ):
    M = 99
    #Помічаєм ребно, що найбільшим значенням
    matrix[nI][nJ]=M
    clearZeroMinus(matrix)
    newMatrix, sumPop = matricReduction(matrix)
    print("+ ", sumPop, " Якщо ми не включаємо ребро ", nI+1, "-", nJ+1, sep="")
    #повертаємо нову редуцьовану матрицю з урахуванням виключенням ребра та сумму на скільки була збільшена нижня межа у порівнянні до виключення ребра
    return newMatrix, sumPop

def ftakeEdge(matrix, nI, nJ):
    M = 99
    #Так як ми беремо ребро nI-nJ, тоді ми повинні виключити зворотне ребро повернення з nJ на nI
    matrix[nJ][nI]=M
    n = len(matrix)
    clearZeroMinus(matrix)
    #Виключаемо всі переходи з вершини nI та переходи на вершину nJ
    for i in range(n):
        matrix[i][nJ]=M
        matrix[nI][i]=M
    newMatrix, sumPop = matricReduction(matrix)
    print("+ ", sumPop, " Якщо ми включаємо ребро ", nI+1, "-", nJ+1, sep="")
    #повертаємо нову редуцьовану матрицю з урахуванням включенням ребра та сумму на скільки була збільшена нижня межа після включення ребра
    return newMatrix, sumPop


def tspSolver(mDis):

    tempArr = matrixCopy(mDis)
    n = len(mDis)
    #знаходимо початкову нижню межу та проводимо редукцію матриці
    mDis, sumDif = matricReduction(tempArr)

    #PriorityQueue буде використовуватися як структура даних для зберігання вузлів (кейсів), яка дозволяє нам витягти кейс з найменьшою нижною межою
    mainPQ = PriorityQueue()
    #Додання першого вузла зі стартової матрици, після 1-ї редукції та мінімальної границі без урахування додання та виключення будь-яких ребр
    mainPQ.put(Node(sumDif, mDis, []))
    itr = 1
    while mainPQ.empty()==False:
        print("#######################################################")
        print("Ітерація ", itr)
        itr+=1

        currQ = mainPQ.get()
        mDis = currQ.matrix
        sumDif = currQ.getSumDif()
        takeEdge = list(currQ.addPair)
        print("нижня границя: ", currQ.getSumDif())
        printEdge(takeEdge)

        #Перевіряємо якщо в даному кейчі (вузлу) залишаеться тільки 1 ребро по якому можна перейти, знаходимо це ребро та отримаємо загальну відповідь
        if len(takeEdge)==len(mDis)-1:
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

        #знаходження максимального значення нульового елемента, а саме в тих клітинках де ми отримали нуль після редукції матриці
        #!!!тобто якщо ми не беремо дане ребро, то сума цільової функції збільшиться (як мінімум) на найбільше мінісове значення
        zeroChange(mDis)
        nI, nJ = findMaxZero(mDis)
        printMatrix(mDis, "Знаходження ребра розголудження (включення та виключення)")
        print("Ребро включення та виключення ", nI+1, "-", nJ+1, sep="")

        #після знаходження максимального ньолового елемента потрібно обнилути всі мінусу для подальних обчислень
        clearZeroMinus(mDis)

        #отримаемо значення нижньої межі при виключенні даного ребра з матриці відстані (маршрута комівояджера)
        print("Виключаємо ребро------------------------------------")
        mDis, newSumDif = fdontTakeEdge(mDis, nI, nJ)
        mDis = matrixCopy(mDis)
        NodeDontTake = Node(sumDif+newSumDif, mDis, takeEdge)
        mainPQ.put(NodeDontTake)

        #отримаемо значення нижньої межі при включенні даного ребра у маршрут комівояджера
        print("Влючаємо ребро---------------------------------------")
        takeEdge = list(currQ.addPair)
        mDis, newSumDif = ftakeEdge(mDis, nI, nJ)
        takeEdge.append([nI, nJ])
        NodeTake = Node(sumDif+newSumDif, mDis, takeEdge)
        mainPQ.put(NodeTake)

if __name__ == "__main__":
    matrixDis = [[99, 4, 5, 6, 6],
                 [5, 99, 4, 5, 4],
                 [3, 7, 99, 5, 6],
                 [4, 3, 5, 99, 6],
                 [7, 4, 4, 5, 99]
                ]
    tspSolver(matrixDis)



