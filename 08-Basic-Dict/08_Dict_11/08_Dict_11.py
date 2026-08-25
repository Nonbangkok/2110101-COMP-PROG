#
# 08_Dict_11: 08_Reverse_n_Keys 
#

def reverse(d):
    return {value:key for key,value in d.items()}
    
    
def keys(d, v):
    return list(key for key,value in d.items() if value ==v)
    

exec(input().strip())