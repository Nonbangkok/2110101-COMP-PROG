#
# 05_List_13: 05_Back_n_Front 
#

l1,l2,l3,res = [],[],[],[]
n = int(input())
l1 = list(input() for _ in range(n))
l2 = list(input().split())
l3 = list((e) for e in iter(input,"-1"))

head = 0
for i in l1 + l2 + l3:
    if head: res.insert(0,i)
    else: res.append(i)
    head ^= 1
