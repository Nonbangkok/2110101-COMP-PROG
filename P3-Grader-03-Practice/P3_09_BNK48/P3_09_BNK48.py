#
# P3_09_BNK48: Part-III-BNK48 
#

scores = {} # (idol,score)
voters = {} # (idol,set_of_distinct_voter)
counts = {} # (voter,idol,score)

while True:
    a = input().split()
    if len(a) == 1: break
    voter,idol,score = a[:]
    scores[idol] = scores.get(idol,0) + int(score)
    voters.setdefault(idol,set()).add(voter)
    counts.setdefault(voter,{})[idol] = counts.get(voter,{}).get(idol,0) + int(score)

if a[0] == '1':
    print(", ".join(item[0] for item in sorted(scores.items(),key=lambda x: -x[1])[:3]))
elif a[0] == '2':
    print(", ".join(item[0] for item in sorted(voters.items(),key=lambda x: -len(x[1]))[:3]))
else:
    count_idol = {}
    for idols in counts.values():
        best,mx = None,0
        for idol,score in idols.items():
            count_idol.setdefault(idol,0)
            if mx < score or (mx == score and best > idol):
                best,mx = idol,score
        count_idol[best] = count_idol.get(best,0) + 1
    print(", ".join(item[0] for item in sorted(count_idol.items(),key=lambda x: -x[1])[:3]))