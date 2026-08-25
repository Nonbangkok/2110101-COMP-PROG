#
# 07_StrFile_13: 07_CamelCase 
#

s = input()
w = "".join(c if c.isalnum() else " " for c in s).split()
