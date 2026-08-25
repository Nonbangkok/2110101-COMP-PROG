#
# 11_NumPy_22: 11_Outer_Product 
#

import numpy as np

def mult_table(nrows, ncols):
    a = np.arange(1,nrows+1)
    a = a[:, None] * np.arange(1,ncols+1)
    return a.reshape(nrows,ncols)

exec(input().strip())