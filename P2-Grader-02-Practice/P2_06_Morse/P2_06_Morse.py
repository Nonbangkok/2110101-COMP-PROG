#
# P2_06_Morse: Part-II-Morse-Code 
#

mp = {}
file_name = input()
file = open(file_name,"r")
lines = file.readlines()
t = lines[0].strip()
if t not in ['T2M','M2T']:
    print("Invalid code")
else:
    a = lines[1].strip().split('[')
    for i in range(1,len(a)-1):
        c = a[i][0]
        m = a[i][2:]
        if t == 'T2M': mp[c] = m
        else: mp[m] = c
    for i in range(2,len(lines)):
        q = lines[i].strip()
        if t == 'M2T': q = q.split()
        res = []
        chk = True
        for c in q:
            if c == ' ': continue
            if c not in mp:
                if t == 'M2T': print(f"Invalid : {" ".join(q)}")
                else: print(f"Invalid : {q}")
                chk = False
                break
            else: res.append(mp[c])
        if chk:
            if t == 'M2T': print("".join(res))
            else: print(" ".join(res))