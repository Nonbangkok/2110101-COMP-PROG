#
# 03_If_02: 03_Change_of_Major 
#

n1 = list(input().split())
n2 = list(input().split())
pass1 = []

if(n1[2] == 'A' and ord(n1[3])-65 <= 2 and ord(n1[4])-65 <= 2):
    pass1.append(n1)
if(n2[2] == 'A' and ord(n2[3])-65 <= 2 and ord(n2[4])-65 <= 2):
    pass1.append(n2)
