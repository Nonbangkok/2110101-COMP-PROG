#
# 07_StrFile_11: 07_Plural 
#

s = input()

if s.endswith('s') or s.endswith('x') or s.endswith('ch'):
    s += 'es'
elif s.endswith('y') and s[-2] not in 'aeiou':
    s = s[:-1] + 'ies'
else:
    s += 's'
