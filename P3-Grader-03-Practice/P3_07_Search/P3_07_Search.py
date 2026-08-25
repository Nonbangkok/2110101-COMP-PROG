#
# P3_07_Search: Part-III-Search-Engine 
#

n = int(input())
docs = []

for i in range(n):
    name,texts = input(),input().split()
    docs.append([name,{}])
    for text in texts:
        docs[i][1][text] = docs[i][1].get(text,0) + 1

while True:
    q = input().strip()
    if q == '-1': break
    mx,idx = 0,-1
    for i in range(n):
        if q not in docs[i][1]: continue
        score = (1/len(docs[i][1])) * (docs[i][1][q]/sum(docs[i][1].values()))
        if mx < score:
            mx = score
            idx = i
    print(docs[idx][0] if idx != -1 else "NOT FOUND")