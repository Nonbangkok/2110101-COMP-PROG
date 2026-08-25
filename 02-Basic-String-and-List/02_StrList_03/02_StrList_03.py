#
# 02_StrList_03: 02_USDate 
#

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
d,m,y = input().split('/')
print(f"{months[int(m)-1]} {d}, {y}")