#
# 05_List_11: 05_MissingDigits 
#

s = input()
res = []
for i in range(10):
    if str(i) not in s:
        res.append(str(i))

print(",".join(res) if len(res) else "None")