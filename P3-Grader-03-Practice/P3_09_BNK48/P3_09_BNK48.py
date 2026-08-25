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
