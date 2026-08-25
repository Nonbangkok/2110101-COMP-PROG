#
# 10_TSD_13: 10_Winner 
#

n = int(input())
matches = [input().split() for _ in range(n)]
winners = {a for a, b in matches} - {b for a, b in matches}
print(sorted(list(winners)))