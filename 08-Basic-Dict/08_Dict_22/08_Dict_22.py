#
# 08_Dict_22: 08_Ice_Cream_Sales 
#

prices = {}
sales = {}
n = int(input())
sum = 0

for i in range(n):
    name,price = input().split()
    prices[name] = float(price)

m = int(input())
for i in range(m):
    name,num = input().split()
    if name not in prices: continue
    sum += prices[name] * int(num)
    sales[name] = sales.get(name,0) + int(num)

ranking = []
for name,num in sales.items():
    ranking.append([-prices[name]*num,name])
ranking.sort()

if sum:
    print(f"Total ice cream sales: {sum}")
    print(f"Top sales: {", ".join([item[1] for item in ranking if item[0] == ranking[0][0]])}")
else:
    print("No ice cream sales")