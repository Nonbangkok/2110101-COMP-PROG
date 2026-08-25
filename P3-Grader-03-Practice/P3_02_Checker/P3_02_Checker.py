#
# P3_02_Checker: Part-III-Giant-Checker 
#

LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

s = input().strip()

if len(s) <= 3:
    row,col = s[:1],s[1:]
else:
    vals = {}
    for p in s.split(','):
        p = p.strip()
        if '=' in p:
            k, v = p.split('=', 1)
            vals[k.strip()] = v.strip()
    row,col = vals.get('row',''),vals.get('col','')