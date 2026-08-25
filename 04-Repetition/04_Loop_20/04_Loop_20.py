#
# 04_Loop_20: 04_ZigZag_2 
#

min_red = None
max_red = None
min_blue = None
max_blue = None

i = 0
while True:
    w = input()
    if len(w.split()) == 1:break
    
    a,b = w.split()
    a = int(a)
    b = int(b)
    
    if i % 2 == 0: r,bl = a,b
    else: r,bl = b,a

    if min_red is None:
        min_red = max_red = r
        min_blue = max_blue = bl
    else:
        if r < min_red: min_red = r
        if r > max_red: max_red = r
        if bl < min_blue: min_blue = bl
        if bl > max_blue: max_blue = bl
    i += 1

if w == "Zig-Zag":
    print(min_red, max_blue)
else:
    print(min_blue, max_red)
