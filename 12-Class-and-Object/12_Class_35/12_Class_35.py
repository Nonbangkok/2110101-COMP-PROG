#
# 12_Class_35: 12_Roman-Numeral 
#

class roman:
    _r_to_i = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
    _i_to_r = [(1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),(100,'C'),(90,'XC'),(50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]

    def __init__(self,r):
        if type(r) == int: self.value = r
        else: self.value = self._roman_to_int(r)

    def _roman_to_int(self, s):
        total = 0
        prev_value = 0
        for char in reversed(s):
            curr_value = self._r_to_i[char]
            if curr_value < prev_value: total -= curr_value
            else: total += curr_value
            prev_value = curr_value
        return total

    def _int_to_roman(self,num):
        if num <= 0: return ""
        result = []
        for value,chars in self._i_to_r:
            while num >= value:
                result.append(chars)
                num -= value
        return "".join(result)

    def __lt__(self, rhs):
        return self.value < rhs.value

    def __str__(self):
        return self._int_to_roman(self.value)

    def __int__(self):
        return self.value

    def __add__(self, rhs):
        return roman(self.value + rhs.value)