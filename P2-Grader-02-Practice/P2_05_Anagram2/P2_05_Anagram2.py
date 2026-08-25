#
# P2_05_Anagram2: Part-II-Anagram-2 
#

a,b = input(),input()
adel = []
bdel = []
afreq = {}
bfreq = {}

a_proceed = "".join(list(c.lower() for c in a if c.isalpha()))
b_proceed = "".join(list(c.lower() for c in b if c.isalpha()))

for c in a_proceed:
    afreq[c]  = afreq.get(c,0) + 1

for c in b_proceed:
    bfreq[c]  = bfreq.get(c,0) + 1

for i in range(26):
    c = chr(97 + i)
    af = afreq.get(c,0)
    bf = bfreq.get(c,0)
    if af > bf: adel.append([c,af-bf])
    elif af < bf: bdel.append([c,bf-af])
 
print(a)
if len(adel):
    for c,cnt in sorted(adel):
        print(f" - remove {cnt} {c}{'\'s' if cnt>1 else ''}")
else:
    print(" - None")
print(b)
if len(bdel):
    for c,cnt in sorted(bdel):
        print(f" - remove {cnt} {c}{'\'s' if cnt>1 else ''}")
else:
    print(" - None")