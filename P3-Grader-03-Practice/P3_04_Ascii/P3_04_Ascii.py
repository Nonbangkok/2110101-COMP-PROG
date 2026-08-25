#
# P3_04_Ascii: Part-III-Ascii-Text 
#

fname,cmd = input(),input()
lines = [l.strip() for l in open(fname).read().splitlines()]
if cmd not in ("LSTRIP","RSTRIP","STRIP","STRIP_ALL"):
    print("Invalid command")
    exit()

if cmd == "STRIP_ALL":
    cols = [c for c in zip(*lines) if set(c) != {'.'}]
    print('\n'.join(''.join(r) for r in zip(*cols)))
else:
    l = min(len(s) - len(s.lstrip('.')) for s in lines) if cmd != "RSTRIP" else 0
    r = min(len(s) - len(s.rstrip('.')) for s in lines) if cmd != "LSTRIP" else 0
    print('\n'.join(''.join(s[l: len(s) - r if r else len(s)]) for s in lines))