#
# 08_Dict_21: 08_Char_Count 
#

s = input().strip()
mp = {}

for c in s.lower():
    if 'a' <= c <= 'z':
        mp[c] = mp.get(c,0) + 1

lst = [[-count, ch] for ch,count in mp.items()]
lst.sort()
