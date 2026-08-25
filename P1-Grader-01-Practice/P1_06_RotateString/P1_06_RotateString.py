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
