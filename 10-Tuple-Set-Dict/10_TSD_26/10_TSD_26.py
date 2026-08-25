#
# 10_TSD_26: 10_Location Analysis 
#

def have_city(a,b):
    for x in a:
        if x in b: return True
    return False

n = int(input())
ids = {}

for i in range(n):
    a = input().split(': ')
    ids[a[0]] = list(a[1].split(', '))

target = input()
res = []
for id,city in ids.items():
    if target != id and have_city(ids[target],city):
        res.append(id)