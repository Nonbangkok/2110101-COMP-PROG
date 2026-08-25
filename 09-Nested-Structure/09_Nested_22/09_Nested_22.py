#
# 09_Nested_22: 09_Matrix 
#

def read_matrix():
    m = []
    nrows = int(input())
    for k in range(nrows):
        x = input().split()
        r = []
        for e in x:
            r.append( float(e) )
        m.append(r)
    return m

def mult_c(c, A):
    for i in range(len(A)):
        for j in range(len(A[0])):
            A[i][j] *= c
    return A
    
def mult(A, B):
    p = len(A)
    q = len(A[0])
    r = len(B[0])
    res = [[0.0 for _ in range(r)] for _ in range(p)]
    for i in range(p):
        for j in range(r):
            for k in range(q):
                res[i][j] += A[i][k] * B[k][j]
    return res
