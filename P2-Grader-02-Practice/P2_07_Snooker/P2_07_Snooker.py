#
# P2_07_Snooker: Part-II-Snooker 
#

colors_score = {'X':0,'R':1,'Y':2,'G':3,'W':4,'B':5,'P':6,'K':7}
score = [0,0]

while True:
    a = input()
    team = int(a[0])
    for i in range(1,len(a)): score[team-1] += colors_score[a[i]]
    if a[1] == 'K': break

print(score[0],score[1])
if score[0] == score[1]: print("Tie")
elif score[0] > score[1]: print("Player 1 wins")
else: print("Player 2 wins")