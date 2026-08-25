#
# 04_Loop_11: 04_RLE 
#

res = []
s = input() + '0'
cnt = 1
for i in range(1,len(s)):
    if s[i] != s[i-1]:
        res.append(s[i-1])
        res.append(str(cnt))
        cnt = 1
    else:
        cnt += 1

print(" ".join(res))