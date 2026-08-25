#
# 03_If_F08: 03_DayOfYear (Function) 
#

def day_of_year(d, m, y):
    y -= 543
    days = [31,28,31,30,31,30,31,31,30,31,30,31]
    if y % 400 == 0 or y % 4 == 0 and y % 100 != 0: days[1] = 29
    return d + sum(days[:m-1])
    
    
exec(input()) # DON'T remove this line