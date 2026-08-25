#
# 03_If_003: 03_Flowchart01 
#

a,b,c,d = list(input().split())
a = int(a)
b = int(b)
c = int(c)
d = int(d)
if a > b:
    a,b = b,a
    if d >= a:
        if c > d:
            c = c - a
    else:
        c = c + a
    b = a + c + d
else:
    if c > a >= b:
        d = d + a
    if d > c:
        b = b + 2
    else:
        b = 2 * b
