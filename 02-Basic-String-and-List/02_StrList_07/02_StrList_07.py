#
# 02_StrList_07: 02_Decryption 
#

s = input()
n1 = s[3::7]
n2 = s[7::5]
n3 = int(n1) + int(n2) + 10000
n4 = str(n3)[-4:-1]
n5 = (int(n4[0]) + int(n4[1]) + int(n4[2])) % 10 + 1
n6 = chr(65 + n5 - 1)