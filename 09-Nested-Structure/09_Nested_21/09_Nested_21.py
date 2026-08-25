#
# 09_Nested_21: 09_Factorization 
#

def factor(N):
    res = []
    for i in range(2,N+1):
        cnt = 0
        while N % i == 0:
               N //= i
               cnt += 1
        if cnt: res.append([i,cnt])
        if N == 1: break
    return res
    
exec(input().strip()) 