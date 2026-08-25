#
# 10_TSD_35: 10_Student Info 
#

n = int(input())
infos = []

for i in range(n):
    infos.append(input().split())
    
q = input().split()

res = []
for info in infos:
    if all(i in info[1:] for i in q):
        res.append(info)
        
print("\n".join(" ".join(info) for info in sorted(res)) if res else "Not Found")
