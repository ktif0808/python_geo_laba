import sys

graph =[[0, 4, 5, 6, 6],
        [5, 0, 4, 5, 4],
        [3, 7, 0, 5, 6],
        [4, 3, 5, 0, 6],
        [7, 4, 4, 5, 0]
        ]
n = 5
visited = [0]*n
answer = 0
answerVer = []

def dfs(v):
    visited[v]=1
    global answer
    minToGo = 9999
    verToGo = -1
    for i in range(n):
        if visited[i]==0:
            if minToGo>graph[v][i]:
                minToGo = graph[v][i]
                verToGo = i
    answer+=graph[v][verToGo]
    answerVer.append(verToGo)
    if len(answerVer)!=n:
        return dfs(verToGo)
    else:
        return verToGo

bestAnswer = 99999
bestPath = []
for i in range(n):
    visited = [0]*n
    print("Відправляємося з вершини", i+1)
    answerVer = [i]
    endV = dfs(i)
    answer+=graph[endV][i]
    answerVer.append(i)
    print("Отримана відповідь: ", answer)
    #print(*list(map(lambda x: x+1, answerVer)))
    print("Послідовність відвідування вершин", *list(map(lambda x: x+1, answerVer)), sep="->")
    if answer<bestAnswer:
        bestAnswer = answer
        bestPath = list(answerVer)
    answer = 0
print("Найкращий результат: ",bestAnswer)
print("Послідовність відвідування вершин", *list(map(lambda x: x+1, bestPath)), sep="->")


