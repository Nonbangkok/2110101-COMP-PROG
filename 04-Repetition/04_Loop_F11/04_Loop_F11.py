#
# 04_Loop_F11: 04_RLE (Function) 
#

def RLE(t):
    res = []
    s = t + '0'
    cnt = 1
    for i in range(1,len(s)):
        if s[i] != s[i-1]:
            res.append([s[i-1],cnt])
            cnt = 1
        else:
            cnt += 1
    return res

exec(input()) # DON'T remove this line