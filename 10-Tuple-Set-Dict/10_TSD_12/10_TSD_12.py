#
# 10_TSD_12: 10_Union Intersection 
#

n = int(input())
mp = dict()

for i in range(n):
    a = set(map(int,input().split()))
    for x in a:
        mp[x] = mp.get(x,0) + 1
