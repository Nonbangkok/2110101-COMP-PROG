#
# 05_List_23: 05_Third_Closest 
#

n = int(input())
a = []
for i in range(n):
    x,y = map(float,input().split())
    a.append([x*x+y*y,i+1,x,y])
a.sort()
