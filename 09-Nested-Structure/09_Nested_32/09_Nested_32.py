#
# 09_Nested_32: 09_FirstFit_BestFit 
#

def first_fit(L, e): # น ำ e ใสรำยกำรย่อยใ ่ น L ด ้วยวิธี first fit
    for l in L:
        if sum(l) + e <= 100:
            l.append(e)
            return;
    L.append([e])

def best_fit(L, e): # น ำ e ใสรำยกำรย่อยใ ่ น L ด ้วยวิธี best fit
    mn_remain = 1e9
    j = -1
    for i in range(len(L)):
        if sum(L[i]) + e <= 100 and 100 - sum(L[i]) < mn_remain:
            mn_remain = 100 - sum(L[i])
            j = i
    if j == -1: L.append([e])
    else: L[j].append(e)

def partition_FF(D): # คืนลิสต์ของลิสต์ที่ได ้จำกกำรแบ่งข ้อมูลใน D ด ้วย first fit
    res = []
    for x in D:
        first_fit(res,x)
    return res

def partition_BF(D): # คืนลิสต์ของลิสต์ที่ได ้จำกกำรแบ่งข ้อมูลใน D ด ้วย best fit
    res = []
    for x in D:
        best_fit(res,x)
    return res

exec(input().strip()) # ตอ้ งมคี ำสั่งนี้ ตรงนี้ตอนสง่ ให้Grader ตรวจ