#
# 08_Dict_12: 08_Nicknames 
#

n = int(input())
d = {}
for i in range(n):
    a,b = input().split()
    d[a],d[b] = b,a

for i in range(int(input())):
    name = input()
    print(d[name] if name in d else "Not found")
