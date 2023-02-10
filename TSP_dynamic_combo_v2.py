import sys




#Вузол дерева, при ініціалізації приймає такі параметри як:
# номер вершини, значення вершини, вершину предка, масив вершин які потрібно посітити,
# силки на вузли вершин які нам потрібно посітити, масив пройденого шляху, матриця (суміжності) відстаней
class Node:
    def __init__(self, ver, value, parent, needVal, arrLink, travelPass, linkGraph):
        self.ver = ver
        self.value = value
        self.needVal = needVal
        self.arrLink = arrLink
        self.travelPass = travelPass
        self.parent = parent
        self.linkGraph = linkGraph



#Рекурента функції обчислення дерева, на спуску рекурсії створює силки на вершини які нам потрібно відвідати,
#а на підйомі сумую пройдений шлях та мінімум у тому разі якщо шляхи перетинаються у вузлу.
def recTSP(root):
    mDis = root.linkGraph
    n =len(mDis)
    #якщо після входу на даний вузол у нас закінчилися вершини які ми повинні відвідати.
    if len(root.needVal)==0:
        #сумуємо вартість ребра повершення в "1" вершину та ребро предка на вершину вузлу
        #!(в контексті роботи даного алгоритма значення на вузлу буде рахуватися не тільки від ребр які зустрічалися на спуску(підйомі) рекурсії
        #а і з урахуванням значення ребра переходу з предка на дану вершину)
        root.value = mDis[root.parent][root.ver]+mDis[root.ver][0]
        return mDis[root.parent][root.ver]+mDis[root.ver][0], [0, root.ver]
    #Перебираемо всі вершини
    for i in range(n):
        #Якщо дана вершина є у списку виршин які комівояджер повинен відвідати для даного вузла
        if i in root.needVal:
            #Створюється новий вузел дерава з вершинами, де вершиною вузла буде вузол "i", а з переліку вершин які потрібно буде вівідати, виключаеться вершина "i"
            tempSet = set(root.needVal)
            tempSet.remove(i)
            tempPath = list(root.travelPass)
            tempPath.append([root.ver, i])
            root.arrLink.append(Node(i, 0, root.ver,  tempSet, [],tempPath, root.linkGraph))
    minVal = sys.maxsize
    needPath = []
    #робимо прохід по вершинам які потрібно відвідати
    for i in root.arrLink:
        #на на виході з рекурсії отримумо вартість марштуру.
        arrR = recTSP(i)
        val = arrR[0]
        path = list(arrR[1])
        #Якщо це не корнева вершина дерева, то ми додаемо варітість переходу з вершини предка на дану вершину вузла
        if root.parent!=-1:
            #Оновлюємо значення екстремуму динаміки на даному вузлу
            if val+mDis[root.parent][root.ver]<minVal:
                minVal = val+mDis[root.parent][root.ver]
                path.append(root.ver)
                needPath = path
        else:
            #Якщо це корнева вершина з якої ми робили запуск рекурентної функції, тоді оновлюємо взначення тільки від значень які були отримані на виході з рекурсії
            if val<minVal:
                minVal = val
                path.append(root.ver)
                needPath = path
    root.value = minVal
    print("сумма подорожі:", root.value, "- W",root.parent+1, list(map(lambda x: x+1, needPath)))
    return root.value, needPath


def tspSolver(matrixDis):
    #запуск динамінки з необхідними нам значеннями
    tsp = recTSP(Node(0,0,-1,{1,2,3,4}, [], [], matrixDis))
    print('відповідь')
    print("Мінімальна вартість ", tsp[0])
    print("Послідовність обхода", *list(map(lambda x: x+1, reversed(tsp[1]))), sep="->")


if __name__ == "__main__":
    matrixDis = [[99, 4, 5, 6, 6],
                 [5, 99, 4, 5, 4],
                 [3, 7, 99, 5, 6],
                 [4, 3, 5, 99, 6],
                 [7, 4, 4, 5, 99]
                ]
    tspSolver(matrixDis)

