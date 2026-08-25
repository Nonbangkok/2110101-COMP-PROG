#
# 10_TSD_33: 10_Polynomial 
#

def add_poly(p1, p2):
    res = {}
    for c,p in p1: res[p] = res.get(p,0) + c
    for c,p in p2: res[p] = res.get(p,0) + c
    return list((c,p) for p,c in sorted(res.items(),reverse=True) if c)
        
def mult_poly(p1, p2):
    res = {}
    for c1,po1 in p1:
        for c2,po2 in p2:
            res[po1+po2] = res.get(po1+po2,0) + c1 * c2
    return list((c,p) for p,c in sorted(res.items(),reverse=True) if c)
