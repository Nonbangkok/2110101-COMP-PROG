#
# 04_Loop_05: 04_CountWord 
#

word = input()
s = input()
for ch in '"(),.\'':
  s = s.replace(ch,' ')
print(s.split().count(word))