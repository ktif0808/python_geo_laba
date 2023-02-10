import sys




def tspSolver(mDis):
    n = len(mDis)
    constMax = sys.maxsize
    dp = [[constMax]*(n) for _ in range(1 << (n))]
    pathD = [[constMax]*(n) for _ in range(1 << (n))]

    dp[1][0]=0
    #Послідовна ітерація через кожну маску.
    for i in range(1, 1<<n):
        #Ітерація по вершинам. Перевіряемо чи у даної маски є вершина в якій запинився комівояджер.
        for j in range(n):
            if dp[i][j]!=constMax:
                #Ітерація по вершинам.Намагаємося знайти вершину в якій ще не побував комівояджер.
                for k in range(1, n):
                    #Додаємо новий біт(вершину) до нашої маски, та перевіряємо чи не були ми в цій вершині.
                    if (i &(1<<k))==0:
                        #Створюємо нову маску.
                        p = i | (1<<k)
                        #Оновлюємо екстремум динаміки на новій масці p та на вершині k, і будуємо масив предків.
                        if dp[i][j]+mDis[j][k] < dp[p][k]:
                            dp[p][k] = dp[i][j]+mDis[j][k]
                            #У масив предків по масці p та  вершині k записуємо вершину з якої ми прийшли.
                            pathD[p][k] = j
    answer = constMax
    last = None
    #З кінцевої маски диниміки (коли всі вершини відвідані) повертаємося в початкове ребро та знаходимо відповідь.
    for i in range(n):
        if dp[(1<<n)-1][i]+mDis[i][0] < answer:
            answer = dp[(1<<n)-1][i]+mDis[i][0]
            #знаходимо вершину з якої ми повернулися на стартову, нам це потрібно для відновлення шляху.
            last = i
    #маска з якої ми побудемо роботи спуск по масиву предків
    cur = (1 << n) - 1
    arAnswer = []
    arAnswer.append(last+1)
    while cur > 1:
        arAnswer.append(pathD[cur][last]+1)
        #отримаємо вершину предка
        temp = pathD[cur][last]
        #віднімаємо біт вершни з маски
        cur=cur - (1<<last)
        last = temp
    arAnswer.reverse()
    print("Найнижча вартість маршруту ", answer)
    print(*arAnswer, "1", sep="->")


if __name__ == "__main__":
    matrixDis = [[99, 4, 5, 6, 6],
                 [5, 99, 4, 5, 4],
                 [3, 7, 99, 5, 6],
                 [4, 3, 5, 99, 6],
                 [7, 4, 4, 5, 99]
                ]
    tspSolver(matrixDis)
