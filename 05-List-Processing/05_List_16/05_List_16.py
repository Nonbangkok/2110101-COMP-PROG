#
# 05_List_16: 05_Collatz 
#

n = int(input())
res = [str(n)]
while n != 1:
    if n & 1: n = 3 * n + 1
    else: n >>= 1
    res.append(str(n))

print("->".join(res[-15:]))