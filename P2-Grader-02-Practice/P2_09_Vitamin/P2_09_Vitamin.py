#
# P2_09_Vitamin: Part-II-Vitamin 
#

n = int(input())
v = []

fruit_names = []
fruits = []

for i in range(n):
    a = input().split()
    fruits.append(a)
    fruit_names.append(a[0])

c = input().split()

if c[0] == 'show': 
    for a in fruits:
        print(" ".join(a))
elif c[0] == 'max':
    m = int(c[1])
    res = []
    mx = 0
    for i in range(len(fruits)):
        if mx < float(fruits[i][m]):
            mx = float(fruits[i][m])
    for i in range(len(fruits)):
        if mx == float(fruits[i][m]):
            res.append(fruits[i][0])
    res.sort()
    print(f"{res[0]} {mx}")
elif c[0] == 'avg':
    m = int(c[1])
    sum = 0
    for i in range(len(fruits)):
        sum += float(fruits[i][m])
    print(round(sum/len(fruits),4))
elif c[0] == 'get':
    if c[1] not in fruit_names: print(f"{c[1]} not found")
    else: print(" ".join(fruits[fruit_names.index(c[1])]))
elif c[0] == 'sort':
    m = int(c[1])
    a = sorted(fruits,key=lambda x: (float(x[m]),x[0]))
    print(" ".join(list(fruit[0] for fruit in a)))