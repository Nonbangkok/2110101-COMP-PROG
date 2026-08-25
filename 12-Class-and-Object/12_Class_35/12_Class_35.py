#
# 12_Class_35: 12_Roman-Numeral 
#

class roman:
    _r_to_i = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
    _i_to_r = [(1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),(100,'C'),(90,'XC'),(50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]

    def __init__(self,r):
        if type(r) == int: self.value = r
        else: self.value = self._roman_to_int(r)

    def _roman_to_int(self,s):
        sum,prev = 0,0
        for c in reversed(s):
            cur = self._r_to_i[c]
            if cur < prev: sum -= cur
            else: sum += cur
            prev = cur
        return sum

    def _int_to_roman(self,num):
        if num <= 0: return ""
        res = []
        for value,c in self._i_to_r:
            while num >= value:
                res.append(c)
                num -= value
        return "".join(res)

    def __lt__(self, rhs):
        return self.value < rhs.value

    def __str__(self):
        return self._int_to_roman(self.value)

    def __int__(self):
        return self.value

    def __add__(self, rhs):
        return roman(self.value + rhs.value)
        
t, r1, r2 = input().split()
a = roman(r1)
b = roman(r2)

if t == '1' : print(a < b)
elif t == '2' : print(int(a),int(b))
elif t == '3' : print(str(a),str(b))
elif t == '4' : print(int(a + b))
else : print(str(a + b))