#
# 05_List_31: 05_Cut_n_Shuffle 
#

s = input().split()
n = len(s)
m = input()

for i in m:
    if i == 'C': s = s[n//2:] + s[:n//2]
    elif i == 'S':
        res = []
        for k,j in zip(s[:n//2],s[n//2:]):
            res.append(k)
            res.append(j)
        s = res
