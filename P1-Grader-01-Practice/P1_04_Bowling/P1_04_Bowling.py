#
# P1_04_Bowling: Part-I-Bowling 
#

def get_score(w,i):
    if w[i] == 'X': return 10
    if w[i] == '/': return 10 - int(w[i-1])
    return int(w[i])

w = input()
n = int(input())
scores = []
frame = 1
score = 0
con = 0
 
for i in range(len(w)):
    #score = 0
    if w[i] == 'X':
        score += get_score(w,i)
        if i+1 < len(w) and frame < 10: score += get_score(w,i+1)
        if i+2 < len(w) and frame < 10: score += get_score(w,i+2)
        if frame < 10: frame += 1
        con = 0
    elif w[i] == '/':
        score += get_score(w,i)
        if i+1 < len(w) and frame < 10: score += get_score(w,i+1)
        if frame < 10: frame += 1
        con = 0
    else:
        con += 1
        if con == 2 and frame < 10:
            frame += 1
            con = 0
        score += get_score(w,i)
        if i == len(w) - 1: frame += 1
    if len(scores) < frame - 1:
        scores.append(score - (sum(scores[:]) if len(scores) else 0))

print(scores[n-1] if 1 <= n <= 10 else score)