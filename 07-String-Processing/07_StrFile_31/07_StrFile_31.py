#
# 07_StrFile_31: 07_DNA 
#

def get_complement(c):
    if c == 'A': return 'T'
    if c == 'T': return 'A'
    if c == 'G': return 'C'
    if c == 'C': return 'G'

def get_index(c):
    if c == 'A': return 0
    if c == 'T': return 1
    if c == 'G': return 2
    if c == 'C': return 3

s = input().strip().upper()
w = input().strip()

def solve():
    for c in s:
        if c not in "ATGC":
          print("Invalid DNA")
          return

    if w == 'R':
        n = list(map(get_complement,s))
        print("".join(n[::-1]))
    elif w == 'F':
        freq = [0] * 4
        for i in s:
            freq[get_index(i)] += 1
        print(f"A={freq[0]}, T={freq[1]}, G={freq[2]}, C={freq[3]}")
    else:
        d = input().strip()
        cnt = 0
        for i in range(len(s)-1):
            if s[i:i+2] == d:
                cnt += 1
        print(cnt)
