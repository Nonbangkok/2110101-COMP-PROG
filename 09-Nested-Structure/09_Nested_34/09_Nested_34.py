#
# 09_Nested_34: 09_Fill_In_Numbers 
#

def pattern1(nrows, ncols): # nrows >= 0, ncols >= 0
    res = []
    for i in range(nrows):
        res.append([])
        for j in range(ncols):
            res[i].append(ncols*i+j+1)
    return res
    
def pattern2(nrows, ncols): # nrows >= 0, ncols >= 0
    res = []
    for i in range(nrows):
        res.append([])
        for j in range(ncols):
            res[i].append(nrows*j+i+1)
    return res
    
def pattern3(N): # N >= 0
    res = []
    for i in range(N):
        res.append([])
        for j in range(N):
            if i <= j: res[i].append(N*i+j+1-(i*(i+1)//2))
            else: res[i].append(0)
    return res
    
def pattern4(N): # N >= 0
    res = []
    for i in range(N):
        res.append([])
        for j in range(N):
            if i <= j: res[i].append(((j+1)*(j+2)//2)-i)
            else: res[i].append(0)
    return res
    
def pattern5(N): # N >= 0
    res = []
    for i in range(N):
        res.append([])
        for j in range(N):
            if i <= j: res[i].append((N*(N+1)//2)-((N-j+i)*((N-j+i)+1)//2)+1+i)
            else: res[i].append(0)
    return res
    
def pattern6(N): # N >= 0
    res = [[0]*N for _ in range(N)]
    val = 1
    for k in range(N):
        length = N - k
        if k % 2 == 0:
            for row in range(length):
                res[row][row+k] = val + row
        else:
            for row in range(length):
                res[row][row+k] = val + (length-1-row)
        val += length
    return res
    
exec(input().strip())