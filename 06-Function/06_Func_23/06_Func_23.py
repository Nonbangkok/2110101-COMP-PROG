#
# 06_Func_23: 06_FourFunctions 
#

def make_int_list(x):
    return list(map(int,x.split()))
    
    
def is_odd(e):
    return e & 1 == 1
    
    
def odd_list(alist):
    return list(x for x in alist if x & 1)
    
    
def sum_square(alist):
    return sum(x*x for x in alist)
    