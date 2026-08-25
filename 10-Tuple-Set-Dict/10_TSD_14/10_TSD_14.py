#
# 10_TSD_14: 10_Database 
#

courses = open(input()).readlines()
teachers = open(input()).readlines()
database = open(input()).readlines()

cmp = {}
for i in range(len(courses)):
    n,a = courses[i].strip().split(',')
    cmp[n] = a
    
tmp = {}
for i in range(len(teachers)):
    n,a = teachers[i].strip().split(',')
    tmp[n] = a

for i in range(len(database)):
    n,m = database[i].strip().split(',')
    if n not in cmp or m not in tmp:
        print("record error")
    else:
        print(f"{cmp[n]},{tmp[m]}")
