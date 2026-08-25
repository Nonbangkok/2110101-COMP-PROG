#
# P2_03_Func2: Part-II-Potpourri-Functions 
#

def convex_polygon_area(p):
    return 0.5*abs(sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p))))
    
def is_heterogram(s):
    p = []
    ss = list(c for c in s if c.isalpha())
    for c in ss:
        if c.lower() in p:
            return False
        p.append(c)
    return True
    
def replace_ignorecase(s, a, b):
    res,i,la = "",0,len(a)
    while i < len(s):
        if s[i:i+la].lower() == a.lower():
            res,i = res+b,i+la
        else:
            res,i = res+s[i],i+1
    return res
        
    
def top3(votes):
    sorted_votes = sorted(votes.items(),key=lambda x: (-x[1],x[0]))
    return list(star[0] for star in sorted_votes[:3])
    
    
for k in range(2):
    exec(input().strip())