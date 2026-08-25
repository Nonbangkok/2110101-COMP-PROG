#
# 04_Loop_F06: 04_PrintTriangle (Function) 
#

def print_triangle(h):
    for i in range(h):
        print('.'*(h-i-1),end='')
        if i == 0: print('*')
        elif i == h-1: print('*'*(2*h-1))
        else: print('*'+(2*i-1)*'.'+'*')
    
    
    
exec(input()) # DON'T remove this line