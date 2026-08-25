#
# P3_04_Ascii: Part-III-Ascii-Text 
#

fname,cmd = input(),input()
text = open(fname).read().splitlines()

if cmd not in ["LSTRIP","RSTRIP","STRIP","STRIP_ALL"]:
    print("Invalid command")
    exit()

mn_left = 1e9
for line in text:
    dot = 0
    for c in line.strip():
        if c != '.':
            mn_left = min(mn_left,dot)
            break
        else: dot += 1

mn_right = 1e9
for line in text:
    dot = 0
    for c in line.strip()[::-1]:
        if c != '.':
            mn_right = min(mn_right,dot)
            break
        else: dot += 1