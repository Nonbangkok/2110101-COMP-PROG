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
