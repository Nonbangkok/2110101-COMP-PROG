#
# P1_03_RSP: Part-I-Rock-Scissor-Paper 
#

m = int(input())
s1,s2,ntie = 0,0,0

while True:
    a = input().split()
    res = -1
    if a[0] == 'R' and a[1] == 'S': res = 0
    if a[0] == 'R' and a[1] == 'P': res = 1
    if a[0] == 'S' and a[1] == 'R': res = 1
    if a[0] == 'S' and a[1] == 'P': res = 0
    if a[0] == 'P' and a[1] == 'R': res = 0
    if a[0] == 'P' and a[1] == 'S': res = 1
    if res == -1: ntie += 1
    elif res == 0: s1 += 1
    else: s2 += 1
    if s1 == m:
        print(s1,s2)
        print("Player 1 wins")
        break
    if s2 == m:
        print(s1,s2)
        print("Player 2 wins")
        break
    if s1 + s2 + ntie == 3*m:
        print(s1,s2)
        print("Tie")
        break
    