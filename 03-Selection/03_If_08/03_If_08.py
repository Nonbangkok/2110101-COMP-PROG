#
# 03_If_08: 03_DayOfYear 
#

d = int(input())
m = int(input())
y = int(input()) - 543
days = [31,28,31,30,31,30,31,31,30,31,30,31]
if y % 400 == 0 or y % 4 == 0 and y % 100 != 0: days[1] = 29