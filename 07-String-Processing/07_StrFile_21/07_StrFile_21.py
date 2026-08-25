#
# 07_StrFile_21: 07_Rot13 
#

def rot13(c):
  if "a" <= c <= "z":
    return chr((ord(c) - ord("a") + 13) % 26 + ord("a"))
  elif "A" <= c <= "Z":
    return chr((ord(c) - ord("A") + 13) % 26 + ord("A"))
  return c

