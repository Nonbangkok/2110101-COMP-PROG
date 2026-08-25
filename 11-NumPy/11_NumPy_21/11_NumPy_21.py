#
# 11_NumPy_21: 11_Slicing and Element-wise Op. 
#

import numpy as np

def sum_2_rows( M ):
    return M[0::2] + M[1::2]

def sum_left_right( M ):
    n = M.shape[0]
    return M[:,:n//2] + M[:,n//2:]

def sum_upper_lower( M ):
    n = M.shape[0]
    return M[:n//2] + M[n//2:]

def sum_4_quadrants( M ):
    n = M.shape[0]
    m = M.shape[1]
    return M[:n//2,:m//2] + M[n//2:,:m//2] + M[:n//2,m//2:] + M[n//2:,m//2:]
    
def sum_4_cells( M ):
    n,m = M.shape
    return M.reshape(n//2,2,m//2,2).sum(axis=(1,3))
    
def count_leap_years( years ):
    years -= 543
    return int(np.sum(((years % 4 == 0) & (years % 100 != 0)) | (years % 400 == 0)))

exec(input().strip())