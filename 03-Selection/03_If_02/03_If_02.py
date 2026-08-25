#
# 03_If_02: 03_Change_of_Major 
#

n1 = list(input().split())
n2 = list(input().split())
pass1 = []

if(n1[2] == 'A' and ord(n1[3])-65 <= 2 and ord(n1[4])-65 <= 2):
    pass1.append(n1)
if(n2[2] == 'A' and ord(n2[3])-65 <= 2 and ord(n2[4])-65 <= 2):
    pass1.append(n2)

if len(pass1) == 0:
    print("None")
elif len(pass1) == 1:
    print(pass1[0][0])
else:
    winner = []
    if n1[1] > n2[1]: winner.append(n1)
    elif n1[1] < n2[1]: winner.append(n2)
    else:
        if ord(n1[3]) < ord(n2[3]): winner.append(n1)
        elif ord(n1[3]) > ord(n2[3]): winner.append(n2)
        else:
            if ord(n1[4]) < ord(n2[4]): winner.append(n1)
            elif ord(n1[4]) > ord(n2[4]): winner.append(n2)
    if len(winner) == 0:
        print("Both")
    else:
        print(winner[0][0])