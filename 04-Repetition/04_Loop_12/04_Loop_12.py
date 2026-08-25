#
# 04_Loop_12: 04_ZigZag_1 
#

n = int(input())
red = []
blue = []

for i in range(n):
    a,b = input().split()
    a = int(a)
    b = int(b)
    if i % 2 == 0:
        red.append(a)
        blue.append(b)
    else:
        red.append(b)
        blue.append(a)

w = input()