#
# 05_List_21: 05_Upgrade 
#

grades = ['A','B+','B','C+','C','D+','D','F']
ids,gs = [],[]
while True:
    a = input()
    if a == 'q': break
    ids.append(a.split()[0])
    gs.append(a.split()[1])

for uid in input().split():
    if gs[ids.index(uid)] == 'A': continue
    gs[ids.index(uid)] = grades[grades.index(gs[ids.index(uid)])-1]
