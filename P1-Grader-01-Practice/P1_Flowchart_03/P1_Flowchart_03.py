#
# P1_Flowchart_03: Part-I-Flowchart-03 
#

import math

a,b,c,d = map(int,input().split())

if a == 1:
    c,d = d,c
    if b == 1: c = c + d
    elif b == 2: c = c - d
    elif b != 3: c = c + c**d
    else: c = c / d
    a = (d + math.sqrt((c / b)**3 + d)) / (2 + b * d)