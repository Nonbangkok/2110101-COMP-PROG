#
# P1_02_RLE: Part-I-RLE 
#

cmd = input()

if cmd == "str2RLE":
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