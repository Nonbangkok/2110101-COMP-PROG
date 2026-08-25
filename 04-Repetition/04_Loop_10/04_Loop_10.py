#
# 04_Loop_10: 04_Bisection_Log10_2 
#

import math

a = float(input())
L = 0
U = int(math.log10(a)) + 1

x = (L + U) / 2
while abs(a- 10**x) > 10**-10*max(a,10**x):
    if 10**x > a: U = x
    elif 10**x < a: L = x
    x = (L + U) / 2

print(round(x,6))