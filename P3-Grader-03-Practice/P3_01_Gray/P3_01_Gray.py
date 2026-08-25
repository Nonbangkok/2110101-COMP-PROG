#
# P3_01_Gray: Part-III-Gray-Codes 
#

n,k=int(input()),int(input())

def solve(n,k):
    if n<1 or k<1:
        print(f"Invalid {'n and k' if n<1 and k<1 else 'n' if n<1 else 'k'}")
        return
    g=[bin(i ^ i >> 1)[2:].zfill(n) for i in range(1 << n)]
    print(''.join(f"{i+1}{'-' * (n - len(str(i+1)) + 1 - (i==k-1))}" for i in range(k)))
    print('\n'.join(','.join(g[i:i+k]) for i in range(0,1 << n,k)))

solve(n,k)