#
# 09_Nested_11: 09_Dedent 
#

n = int(input())
for i in range(n):
    a = input()
    sz = len(a)-len(a.lstrip('.'))
    print('.'*(sz//2)+a.lstrip('.'))