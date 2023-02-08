import sys

n = 5
v = [[0, 4, 5, 6, 6],
     [5, 0, 4, 5, 4],
     [3, 7, 0, 5, 6],
     [4, 3, 5, 0, 6],
     [7, 4, 4, 5, 0]
    ]
constMax = 10**10
dp = [[constMax]*(n) for _ in range(1 << (n))]
pathD = [[constMax]*(n) for _ in range(1 << (n))]

dp[1][0]=0
for i in range(1, 1<<n):
    for j in range(n):
        if dp[i][j]!=constMax:
            for k in range(1, n):
                if (i &(1<<k))==0:
                    p = i | (1<<k)
                    if dp[i][j]+v[j][k] < dp[p][k]:
                        dp[p][k] = dp[i][j]+v[j][k]
                        pathD[p][k] = j
answer = constMax
last = None
for i in range(n):
    if dp[(1<<n)-1][i]+v[i][0] < answer:
        answer = dp[(1<<n)-1][i]+v[i][0]
        last = i
cur = (1 << n) - 1
arAnswer = []
arAnswer.append(last+1)
while cur > 1:
    arAnswer.append(pathD[cur][last]+1)
    temp = pathD[cur][last]
    cur=cur - (1<<last)
    last = temp
arAnswer.reverse()
print("Найнижча вартість маршруту ", answer)
print(*arAnswer, "1", sep="->")
