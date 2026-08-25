#
# P3_03_Text: Part-III-Text-Formatting 
#

fname = input().strip()
k = int(input())

r = ''
for i in range(k // 10):
    r += '-' * 9 + str(i + 1)
if k % 10: r += '-' * (k % 10)
print(r)

text = '.'.join(open(fname).read().splitlines())
tokens,cur,i,n = [],'',0,len(text)

while i < n:
    if text[i] == '.':
        j = i
        while j < n and text[j] == '.':
            j += 1
        tokens.append(cur)
        tokens.append(text[i:j])
        cur = ''
        i = j
    else:
        cur += text[i]
        i += 1
        
tokens.append(cur)
words,seps = tokens[0::2],tokens[1::2]
out,cur = [],words[0]

for w, sep in zip(words[1:], seps):
    cand = cur + sep + w
    if len(cand) <= k:
        cur = cand
    else:
        out.append(cur)
        cur = w