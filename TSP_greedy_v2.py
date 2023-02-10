import sys



#обираємо серед невідвіданих вершин найдешевшу та за допомогою методу пошуку в глибину спускаемося на цю вершину.
def dfsTSP(v, mDis, visited, pathD, answerAdd):

    #відмічаємо, що вершина v вже відвідана.
    n = len(mDis)
    visited[v]=1
    minToGo = sys.maxsize
    verToGo = -1
    #Цикл по всім вершинам та знаходження найдешевної з невідвіданих
    for i in range(n):
        if visited[i]==0:
            if minToGo>mDis[v][i]:
                minToGo = mDis[v][i]
                verToGo = i
    answerAdd[0]+=mDis[v][verToGo]
    pathD.append(verToGo)
    #Якщо ми не посітили n вершин, робимо рекурсивний спуск у глибину для запуску рекурсивної функції від нової вершини
    if len(pathD)!=n:
        return dfsTSP(verToGo, mDis, visited, pathD, answerAdd)
    #Якщо ми відвідали всі n вершин, то вертаємо вершину на якій зупинился
    else:
        return verToGo

def tspSolver(mDis):
    global answer
    n = len(mDis)
    bestAnswer = sys.maxsize
    bestPath = []
    #Будемо запускати метод жадібного алгоритму на усіх n вершинах
    for i in range(n):
        print("#####################################")
        print("Відправляємося з вершини", i+1)
        #оновлюємо масив відвіданих вершин та масив порядку відвідування вершин
        pathD = [i]
        answer = [0]
        visited = [0]*n
        #вертаємо з рекурсивної функції останю вершину на якій зупинилися та робимо повернення на стартову вершину
        endV = dfsTSP(i, mDis, visited, pathD, answer)
        answer[0]+=mDis[endV][i]
        pathD.append(i)
        print("Отримана відповідь: ", answer[0])
        print("Послідовність відвідування вершин", *list(map(lambda x: x+1, pathD)), sep="->")
        #шукаємо найдешевший маршрут комівояджера та оновлюємо відповідь
        if answer[0]<bestAnswer:
            bestAnswer = answer[0]
            bestPath = list(pathD)
        answer = 0
    print("#####################################")
    print("Найкращий результат: ",bestAnswer)
    print("Послідовність відвідування вершин", *list(map(lambda x: x+1, bestPath)), sep="->")


if __name__ == "__main__":
    matrixDis = [[99, 4, 5, 6, 6],
                 [5, 99, 4, 5, 4],
                 [3, 7, 99, 5, 6],
                 [4, 3, 5, 99, 6],
                 [7, 4, 4, 5, 99]
                ]
    tspSolver(matrixDis)


