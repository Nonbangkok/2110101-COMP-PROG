#
# 04_Loop_06: 04_PrintTriangle 
#

n = int(input())

for i in range(n):
    print('.'*(n-i-1),end='')
    if i == 0: print('*')
    elif i == n-1: print('*'*(2*n-1))
    else: print('*'+(2*i-1)*'.'+'*')