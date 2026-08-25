#
# 03_If_09: 03_Biorhythm 
#

import math

def count_days_with_same_year(sd,sm,ed,em,y):
    days = [31,28,31,30,31,30,31,31,30,31,30,31]
    if y % 400 == 0 or (y % 4 == 0 and y % 100 != 0): days[1] = 29
    s = sd + sum(days[:sm-1])
    e = ed + sum(days[:em-1])
    return e - s

bd,bm,by,d,m,y = [int(e) for e in input().split()]
by -= 543
y -= 543
red = count_days_with_same_year(bd,bm,31,12,by) + 1
black = (y - by - 1) * 365
blue = count_days_with_same_year(1,1,d,m,y)
sum_d = red + black + blue