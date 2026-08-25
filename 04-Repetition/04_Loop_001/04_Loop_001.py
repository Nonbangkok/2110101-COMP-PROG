#
# 04_Loop_001: 04_BirthdayParadox (flowchart) 
#

p = float(input())
k = 1
t = 1
t = t*(365-(k-1))/365
while 1 - t < p:
    k += 1
    t = t*(365-(k-1))/365