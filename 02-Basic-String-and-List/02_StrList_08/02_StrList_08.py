#
# 02_StrList_08: 02_Decimal2Fraction 
#

import math

n = input().split(',')
d = int(n[0]+n[1]+n[2])
a = int((d*10**len(n[2]) + int(n[2]) - d) // 10**len(n[2]))
b = (10**len(n[2])-1) * (10**len(n[1]))
gcd = math.gcd(a,b)
print(f"{int(a//gcd)} / {int(b//gcd)}")