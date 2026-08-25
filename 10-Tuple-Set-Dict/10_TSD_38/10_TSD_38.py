#
# 10_TSD_38: 10_Sky Train 
#

adj = {}
while True:
    a = input().split()
    if len(a) == 1: break
    if a[0] not in adj: adj[a[0]] = []
    if a[1] not in adj: adj[a[1]] = []
    adj[a[0]].append(a[1])
    adj[a[1]].append(a[0])

res = set()
res.add(a[0])
for v in adj.get(a[0],[]):
    res.add(v)
    for w in adj.get(v,[]):
        res.add(w)

print("\n".join(sorted(res)))