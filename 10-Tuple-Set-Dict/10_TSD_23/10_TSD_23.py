#
# 10_TSD_23: 10_GenreTotalPlaytime 
#

n = int(input())
songs = []
times = []

for i in range(n):
    a = input().split(', ')
    time = a[-1].split(':')
    time = int(time[0].strip()) * 60 + int(time[1].strip())
    song = a[-2].strip()
    if not song in songs:
        songs.append(song)
        times.append([0,song])
    times[songs.index(song)][0] += time

times.sort(reverse=True)
print("\n".join(f"{b} --> {a//60}:{a%60:02}" for a,b in times[:3]))