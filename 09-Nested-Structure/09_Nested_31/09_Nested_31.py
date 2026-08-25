#
# 09_Nested_31: 09_Pythagorean_Triple 
#

def gcd(a,b):
    while b != 0: a,b = b, a%b
    return a

def is_coprime(a,b,c):
    return gcd(gcd(a, b), c) == 1

def primitive_Pythagorean_triples(max_len):
    res = []
    for c in range(5,max_len+1):
        for a in range(3,c):
            b = int((c*c-a*a)**0.5)
            if b < a or b*b != c*c-a*a or not is_coprime(a,b,c): continue
            res.append([a,b,c])
    return res

exec(input().strip())