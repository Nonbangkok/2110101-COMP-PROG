#
# 05_List_F11: 05_MissingDigits (Function) 
#

def missing_digits(t):
    res = []
    for i in range(10):
        if str(i) not in t:
            res.append(i)
    return res
    
    
exec(input()) # DON'T remove this line