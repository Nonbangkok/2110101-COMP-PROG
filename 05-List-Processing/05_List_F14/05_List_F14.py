#
# 05_List_F14: 05_Peaks (Function) 
#

def peaks(x):
    return list(i for i in range(1,len(x)-1) if x[i-1] < x[i] > x[i+1])
