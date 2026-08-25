#
# P1_05_Golf: Part-I-Golf 
#

import math

p,st,stp =[],[],[]

for i in range(9):
    a,b,c = map(int,input().split())
    p.append(a)
    st.append(b)
    if c: stp.append(min(a+2,b))

t = math.floor(0.8*(1.5*sum(stp)-sum(p)))