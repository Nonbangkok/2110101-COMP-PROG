#
# 08_Dict_24: 08_Texting 
#

def text2keys(text):
    text = "".join(c for c in text if c.isalpha() or c.isspace()).lower()
    groups = ["abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"]
    press = [str(d) * (i + 1) for d, g in enumerate(groups,start=2) for i in range(len(g))]
    res = []
    
    for c in text:
        if c == ' ':
            res.append('0')
        else:
            n = ord(c) - ord('a')
            res.append(press[n])
    
    return " ".join(res)
    
def keys2text(keys):
    groups = ["abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"]
    press = [str(d) * (i + 1) for d, g in enumerate(groups,start=2) for i in range(len(g))]
    res = []
    
    for k in keys.split():
        if k == '0':
            res.append(' ')
        else:
            res.append(chr(press.index(k)+ord('a')))
    
    return "".join(res)