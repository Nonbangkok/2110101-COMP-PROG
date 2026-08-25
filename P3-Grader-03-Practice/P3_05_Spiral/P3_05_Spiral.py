#
# P3_05_Spiral: Part-III-Spiral-Square 
#

def spiral_square(n): # n is a positive odd number
    a = [[0]*n for _ in range(n)]
    d = [[0,1],[-1,0],[0,-1],[1,0]]
    i,j,k = n//2,n//2,0
    val,step = 1,1
    a[i][j] = val
    while val != n*n:
        for _ in range(2):
            for _ in range(step):
                a[i][j] = val
                if val == n*n: break
                val += 1
                i,j = i+d[k%4][0],j+d[k%4][1]
            k += 1    
        step += 1
    return a
 
def print_square(S):
    for i in range(len(S)):
        print(' '.join([(2*' '+str(e))[-3:] for e in S[i]]))

exec(input().strip())