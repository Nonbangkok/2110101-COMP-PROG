#
# 11_NumPy_11: 11_Indexing_and_Slicing 
#

import numpy as np

# A is a 2-d array
def get_column_from_bottom_to_top( A, c ):
    return A[:,c][::-1]
    
def get_odd_rows( A ):
    return A[1::2]
    
def get_even_column_last_row( A ):
    return A[-1,::2]
    
def get_diagonal1( A ): # A is a square matrix
    return np.diag(A)
    
def get_diagonal2( A ): # A is a square matrix
    # from top-right corner down to bottom-left corner
    return np.diag(np.fliplr(A))
    
    
exec(input().strip())