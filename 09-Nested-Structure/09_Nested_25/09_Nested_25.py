#
# 09_Nested_25: 09_Tiling_Puzzle 
#

def row_number(t, e): # return row number of t containing e (top row is row #0)
    for i in range(len(t)):
        if e in t[i]:
            return i
    
def flatten(t): # return a list of ints converted from list of lists of ints t
    return [item for s in t for item in s if item]
    
def inversions(x): # return the number of inversions of list x
    cnt = 0
    for i in range(len(x)):
        for j in range(i):
            if x[j] > x[i]:
                cnt += 1
    return cnt
    
def solvable(t): # return True if tiling t (list of lists of ints) is solvable
    n = len(t)
    x = flatten(t)
    if n % 2 == 1 and inversions(x) % 2 == 0: return True
    if n % 2 == 0 and (inversions(x) + row_number(t,0)) % 2 == 1: return True
    return False

exec(input().strip()) # do not remove this line