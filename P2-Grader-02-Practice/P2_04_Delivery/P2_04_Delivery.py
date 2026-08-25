#
# P2_04_Delivery: Part-II-Delivery 
#

dtype = {'E':1,'Q':3,'N':7,'F':14}

deli = []

def is_leap_year(y):
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)

def valid_date(d, m, y):
    max_days = [31, 29 if is_leap_year(y) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if y < 1 or m < 1 or m > 12 or d < 1: return False
    if d > max_days[m - 1]:return False
    return True

def check_error(id,t,d1,m1,y1):
    chk = 0
    msg = f"Error: {id} {t} {d1} {m1} {y1+543} --> "
    if y1 < 2015:
        chk = 1
        msg += "Invalid year"
    elif not 1 <= m1 <= 12:
        chk = 1
        msg += "Invalid month"
    elif not valid_date(d1,m1,y1):
        chk = 1
        msg += "Invalid date"
    elif t not in dtype:
        chk = 1
        msg += "Invalid delivery type"
    return chk,msg

def next_days(d,m,y,add):
    max_days = [31, 29 if is_leap_year(y) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    d += add
    if d > max_days[m-1]:
        d -=  max_days[m-1]
        m += 1
    if m == 13:
        m = 1
        y += 1
    return d,m,y

while True:
    a = input()
    if a == 'END': break
    
    id,t,d1,m1,y1 = a.split()
    d1,m1,y1 = map(int,[d1,m1,y1])
    y1 -= 543
    chk,msg = check_error(id,t,d1,m1,y1)
    
    if chk:
        print(msg)
    else:
        d2,m2,y2 = next_days(d1,m1,y1,dtype[t])
        deli.append([y2+543,m2,d2,id])
