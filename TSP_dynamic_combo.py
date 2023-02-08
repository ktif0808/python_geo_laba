import sys

v = [[0, 4, 5, 6, 6],
     [5, 0, 4, 5, 4],
     [3, 7, 0, 5, 6],
     [4, 3, 5, 0, 6],
     [7, 4, 4, 5, 0]
    ]
M = 999

#Вузол дерева
class Node:
    def __init__(self, ver, value, parent, needVal, arrLink, travelPass, findPath):
        self.ver = ver
        self.value = value
        self.needVal = needVal
        self.arrLink = arrLink
        self.travelPass = travelPass
        self.parent = parent
        self.findPath = findPath


#Рекурента функції обчислення дерева.
def rec(root):
    if len(root.needVal)==0:
        root.value = v[root.parent][root.ver]+v[root.ver][0]
        return v[root.parent][root.ver]+v[root.ver][0], [0, root.ver]
    for i in range(5):
        if i in root.needVal:
            tempSet = set(root.needVal)
            tempSet.remove(i)
            tempPath = list(root.travelPass)
            tempPath.append([root.ver, i])
            root.arrLink.append(Node(i, 0, root.ver,  tempSet, [],tempPath, [] ))
    minVal = M
    needPath = []
    for i in root.arrLink:
        arrR = rec(i)
        val = arrR[0]
        path = list(arrR[1])
        if root.parent!=-1:
            if val+v[root.parent][root.ver]<minVal:
                #print("#", minVal, val+v[root.parent][root.ver])
                minVal = val+v[root.parent][root.ver]
                path.append(root.ver)
                needPath = path
            #printRes([root.ver,  arrR])
        else:
            if val<minVal:
                minVal = val
                path.append(root.ver)
                needPath = path
        #printRes([root.ver,  arrR])

    root.value = minVal
    print("сумма подорожі:", root.value, "- W",root.parent+1, list(map(lambda x: x+1, needPath)))
    return root.value, needPath

if __name__ == "__main__":
    TSP = rec(Node(0,0,-1,{1,2,3,4}, [], [], []))
    print('відповідь')
    print("Мінімальна вартість ", TSP[0])
    print("Послідовність обхода", *list(map(lambda x: x+1, reversed(TSP[1]))), sep="->")
