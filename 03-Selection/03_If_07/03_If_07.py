#
# 03_If_07: 03_AbbrevNum 
#

n = int(input())
if n < 1000:
    t = n
elif n < 10**4:
    t = str(round(n/10**3,1)) + 'K'
elif n < 10**6:
    t = str(round(n/10**3)) + 'K'
elif n < 10**7:
    t = str(round(n/10**6,1)) + 'M'
elif n < 10**9:
    t = str(round(n/10**6)) + 'M'
elif n < 10**10:
    t = str(round(n/10**9,1)) + 'B'
else:
    t = str(round(n/10**9)) + 'B'
print(t)