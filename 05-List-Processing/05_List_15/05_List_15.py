#
# 05_List_15: 05_UniqueCount 
#

a = sorted(list(map(int,input().split())))
u = [a[0]]
for i in a:
    if i != u[-1]:
        u.append(i)