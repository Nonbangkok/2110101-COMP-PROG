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

row_ok = len(row) == 1 and row.isalpha()
try:
    c = int(col)
    col_ok = 1 <= c <= 52
except ValueError:
    col_ok = False

if not row_ok and not col_ok:
    print("Invalid row and column")
elif not row_ok:
    print("Invalid row")
elif not col_ok:
    print("Invalid column")
else:
    r = LETTERS.find(row)
    print("Black" if (r + c) % 2 == 0 else "White")