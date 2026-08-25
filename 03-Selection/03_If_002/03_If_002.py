#
# 03_If_002: 03_Next15Days (flowchart) 
#

n_days_in_month = [31,0,31,30,31,30,31,31,30,31,30,31]

d,m,y = [int(e) for e in input().split()]
y = y - 543
n = 31

if n_days_in_month[m-1] == 30:
    n = 30
else:
    if m == 2:
        n = 28
        if y % 400 == 0:
            n = 29
        if y % 4 == 0 and y % 100 != 0:
            n = 29

d = d + 15
if d > n:
    d = d - n
    m = m + 1
if m > 12:
    m = m - 12
    y = y + 1
y = y + 543