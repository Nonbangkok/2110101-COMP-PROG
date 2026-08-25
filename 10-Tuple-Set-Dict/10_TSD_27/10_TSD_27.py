#
# 10_TSD_27: 10_Celebrity 
#

def knows(R,x,y):
    return y in R[x]
    
def is_celeb(R,x):
    if len(R[x]) and not (len(R[x])==1 and list(R[x])[0]==x) : return False
    for name,r in R.items():
        if name == x: continue
        #for y in r:
        #    if not knows(R,y,x): return False
        if x not in r: return False
    return True
    
def find_celeb(R):
    for i in R:
        if is_celeb(R,i): return i
    return None
    
def read_relations():
    R = dict()
    while True:
        d = input().split()
        if len(d) == 1: break
        if d[0] not in R: R[d[0]] = set()
        if d[1] not in R: R[d[1]] = set()
        R[d[0]].add(d[1])
    return R

def main():
    R = read_relations()
    c = find_celeb(R)
    if c == None :
        print('Not Found')
    else:
        print(c)
