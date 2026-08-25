#
# 11_NumPy_23: 11_Lower_than_Mean 
#

import numpy as np

def read_data():
    w = [float(e) for e in input().split()]
    weight = np.array(w)
    n = int(input())
    data = np.ndarray((n, 4), int)
    for i in range(n):
        data[i] = [int(e) for e in input().split()]
    return weight, data
    
def report_lower_than_mean(weight, data):
    names = data[:,0]
    values = data[:,1:].astype(float)
    scores = np.sum(values*weight,axis=1)
    mean = np.mean(scores)
    print(", ".join(names[scores<mean].astype(str)) if len(names[scores<mean]) else "None")

exec(input().strip())