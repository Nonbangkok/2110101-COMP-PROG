#
# P2_08_Thai: Part-II-Thai-Numeral 
#

def to_Thai(N):
    pn = ["soon","neung","song","sam","si","ha","hok","chet","paet","kao"]
    res = []
    if N <= 9: return pn[N]
    if N >= 1000:
        res.append(pn[N//1000]+" pun")
        N %= 1000
    if N >= 100:
        res.append(pn[N//100]+" roi")
        N %= 100
    if N >= 10:
        t = N // 10
        if t == 1: res.append("sip")
        elif t == 2: res.append("yi sip")
        else: res.append(pn[t] + " sip")
        N %= 10
    if N == 1: res.append("et")
    elif N >= 2: res.append(pn[N])
    return  ' '.join(res)
    