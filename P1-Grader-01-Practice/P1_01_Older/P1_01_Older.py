#
# P1_01_Older: Part-I-Older 
#

a = input().split()
b = input().split()

def compare(a,b):
    if int(a[-1]) < int(b[-1]): return a[0]
    if int(a[-1]) > int(b[-1]): return b[0]
    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    if months.index(a[1]) < months.index(b[1]): return a[0]
    if months.index(a[1]) > months.index(b[1]): return b[0]
    if int(a[2][:-1]) < int(b[2][:-1]): return a[0]
    if int(a[2][:-1]) > int(b[2][:-1]): return b[0]
    return f"{a[0]} {b[0]}"