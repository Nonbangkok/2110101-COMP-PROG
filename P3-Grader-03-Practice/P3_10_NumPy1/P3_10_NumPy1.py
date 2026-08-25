#
# P3_10_NumPy1: Part-III-NumPy-Functions 
#

import numpy as np

def eq(A, B, p):
    return (np.sum(A==B)/A.size*100) >= p

def closest_point_indexes(points, p):
    dis = np.sum((points-p)**2,axis=1)
    mn = np.min(dis)
    return np.where(dis == mn)[0]

def number_of_inversions(A):
    i,j = np.triu_indices(len(A),k=1)
    return np.sum(A[i] > A[j])