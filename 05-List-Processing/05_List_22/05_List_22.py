#
# 05_List_22: 05_Upgrade_2 
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

p = list(zip(ids,gs))
p.sort()

for i in p:
    print(i[0],i[1])