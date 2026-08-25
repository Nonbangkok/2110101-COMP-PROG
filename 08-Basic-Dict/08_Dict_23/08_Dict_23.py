#
# 08_Dict_23: 08_Telephone_Directory 
#

n = int(input())
mp = {}

for i in range(n):
    a = input().split()
    mp[a[0]+' '+a[1]] = a[2]
    mp[a[2]] = a[0] + ' ' + a[1]
