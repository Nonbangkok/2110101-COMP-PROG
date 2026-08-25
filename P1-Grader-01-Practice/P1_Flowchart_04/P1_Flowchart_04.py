#
# P1_Flowchart_04: Part-I-Flowchart-04 
#

X1 = input().strip()
X2 = input().strip()
X3 = input().strip()

X = X1 + X2 + X3

if len(X) != 9:
    print("ERROR")
else:
    win = "-"
    i = 0
    while i < 3:
        if X[3*i] == X[3*i+1] == X[3*i+2]:
            win = X[3*i]
            break
        if X[i] == X[i+3] == X[i+6]:
            win = X[i]
            break
        i += 1

    if win == "-":
        if X[0] == X[4] == X[8]: win = X[0]
        if X[3] == X[4] == X[6]: win = X[6]

    if win == "-": print("???")
    else: print(win)