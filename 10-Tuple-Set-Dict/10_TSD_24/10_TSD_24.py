#
# 10_TSD_24: 10_Cartoon 
#

cartoons = []
names = {}

while True:
    a = input()
    if a == 'q': break
    a = a.split(', ')
    if a[1] not in cartoons:
        cartoons.append(a[1])
        names[a[1]] = []
    names[a[1]].append(a[0])
