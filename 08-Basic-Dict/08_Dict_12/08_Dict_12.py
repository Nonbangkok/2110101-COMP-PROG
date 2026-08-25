#
# 08_Dict_12: 08_Nicknames 
#

n = int(input())
d = {}
for i in range(n):
    a,b = input().split()
    d[a],d[b] = b,a

