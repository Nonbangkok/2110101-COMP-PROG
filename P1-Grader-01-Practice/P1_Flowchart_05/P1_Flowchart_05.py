#
# P1_Flowchart_05: Part-I-Flowchart-05 
#

import math

c = input()

if c == 'S':
    m = int(input())
    q,r,t,k,n,x = 1,0,1,1,3,3
    i = 0
    p = ""
    while i < m:
        if 4*q + r - t < n*t:
            p = p + str(n)
            i = i + 1
            a = 10*(r - n*t)
            n = (10*(3*q + r))//t - 10*n
            q = 10*q
            r = a
        else:
            a = (2*q + r)*x
            b = (7*q*k + 2 + x*r)//(x*t)
            q = k*q
            t = x*t
            x = x + 2
            k = k + 1
            n = (a + b)//t
            r = a
    p = p[0] + '.' + p[1:]
    print('pi =', p)

elif c == 'R':
    n = int(input())
    p = math.sqrt(12) * sum(((-3)**(-k)) / (2*k + 1) for k in range(n + 1))
    p = round(p, 12)
    print('pi =', p)

elif c == 'P':
    p = math.sqrt(7 + math.sqrt(6 + math.sqrt(5)))
    p = round(p, 6)
    print('pi =', p)

else:
    print('Invalid')