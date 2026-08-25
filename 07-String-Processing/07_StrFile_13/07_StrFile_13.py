#
# 07_StrFile_13: 07_CamelCase 
#

s = input()
w = "".join(c if c.isalnum() else " " for c in s).split()
print(w[0].lower()+"".join(x.capitalize() for x in w[1:]))
