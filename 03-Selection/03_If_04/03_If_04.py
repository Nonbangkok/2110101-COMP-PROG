#
# 03_If_04: 03_MobileNumber 
#

n = input()
prefix = ["06","08","09"]

print("Mobile number" if len(n) == 10 and n[:2] in prefix else "Not a mobile number")