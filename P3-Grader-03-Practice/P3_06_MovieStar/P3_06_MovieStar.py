#
# P3_06_MovieStar: Part-III-Movie-Stars 
#

n = int(input())
movies = {}

for i in range(n):
    a = input().split(', ')
    for j in range(1,len(a)):
        if a[j] not in movies:
            movies[a[j]] = []
        movies[a[j]].append(a[0])