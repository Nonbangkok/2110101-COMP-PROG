#
# P3_08_Bidding: Part-III-Bidding 
#

n = int(input())
bid,res = {},{}
names = set()

for i in range(n):
    a = input().split()
    if a[0] == 'B':
        user,prod,price = a[1:]
        names.add(user)
        bid[prod] = [b for b in bid.get(prod,[]) if b[0] != user]
        bid.setdefault(prod,[]).append([user,int(price)])
    elif a[0] == 'W':
        user,prod = a[1:]
        bid[prod] = [b for b in bid.get(prod,[]) if b[0] != user]


for prod,b in bid.items():
    user,mx = "",0
    for i in range(len(b)):
        if mx < b[i][1]:
            mx = b[i][1]
            user = b[i][0]
    res.setdefault(user,[]).append([prod,mx])