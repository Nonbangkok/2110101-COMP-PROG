#
# 05_List_31: 05_Cut_n_Shuffle 
#

s = input().split()
n = len(s) // 2
m = input()

for i in m:
    if i == 'C': s = s[n:] + s[:n]
    elif i == 'S': s = [x for p in zip(s[:n],s[n:]) for x in p]

print(' '.join(s))