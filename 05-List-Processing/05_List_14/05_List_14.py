#
# 05_List_14: 05_Peaks 
#

a = list(map(int,input().split()))
print(sum(a[i-1] < a[i] > a[i+1] for i in range(1,len(a)-1)))