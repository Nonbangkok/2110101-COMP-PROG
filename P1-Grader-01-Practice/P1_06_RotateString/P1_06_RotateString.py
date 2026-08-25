#
# P1_06_RotateString: Part-I-RotateString 
#

rotate = input()
n = int(input())
m = None
a = []
chk = True

for i in range(n):
    a.append(input())
    if m is None: m = len(a[0])
    elif m != len(a[-1]): chk = False

if chk:
    if rotate == '90':
        for j in range(m):
            for i in range(n-1,-1,-1):
                print(a[i][j],end='')
            print()
    elif rotate == 'flip':
        for i in range(n):
            for j in range(m-1,-1,-1):
                print(a[i][j],end='')
            print()
    else:
        for i in range(n-1,-1,-1):
            for j in range(m-1,-1,-1):
                print(a[i][j],end='')
            print()
else:
    print("Invalid size")