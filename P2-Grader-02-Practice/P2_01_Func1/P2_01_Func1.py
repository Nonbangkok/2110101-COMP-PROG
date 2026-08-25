#
# P2_01_Func1: Part-II-Odd-Odd-Functions 
#

def is_odd(n):
    return bool(n & 1)
    
def has_odds(x):
    return any(n & 1 for n in x)
    
def all_odds(x):
    return all(n & 1 for n in x)
    
def no_odds(x):
    return not any(n & 1 for n in x)
    
def get_odds(x):
    return list(n for n in x if n & 1)
    
def zip_odds(a, b):
    a = get_odds(a)
    b = get_odds(b)
    c = []
    i,j = 0,0
    
    while i < len(a) and j < len(b):
         c.append(a[i])
         c.append(b[j])
         i += 1
         j += 1
        
    while i < len(a):
        c.append(a[i])
        i += 1
    while j < len(b):
        c.append(b[j])
        j += 1
        
    return c
