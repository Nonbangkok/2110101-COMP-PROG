#
# 08_Dict_23: 08_Telephone_Directory 
#

n = int(input())
mp = {}

for i in range(n):
    a = input().split()
    mp[a[0]+' '+a[1]] = a[2]
    mp[a[2]] = a[0] + ' ' + a[1]

m = int(input())
for i in range(m):
    a = input().split()
    if len(a) == 1:
        print(f"{a[0]} --> {mp[a[0]] if a[0] in mp else 'Not found' }")
    else:
        print(f"{a[0]} {a[1]} --> {mp[a[0]+' '+a[1]] if a[0]+' '+a[1] in mp else 'Not found' }")
