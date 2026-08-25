#
# 03_If_03: 03_Gymnastic_Score 
#

a = input().split()
a.sort()
print(f"{round((float(a[1])+float(a[2]))/2,2)}")