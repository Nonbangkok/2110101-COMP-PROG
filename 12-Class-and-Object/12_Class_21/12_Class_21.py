#
# 12_Class_21: 12_Complex-Number 
#

class Complex :
    def __init__(self,a,b):
        self.a = a
        self.b = b

    def __str__(self):
        if self.a==0 and self.b==0: return "0"
        return f"{self.a if self.a != 0 else ''}{'+' if self.b > 0 and self.a != 0 else ''}{'-' if self.b == -1 else ''}{self.b if self.b != 0 and abs(self.b) != 1 else ''}{'i' if self.b != 0 else ''}"
     
    def __add__(self, rhs):
        return Complex(self.a+rhs.a,self.b+rhs.b)
     
    def __mul__(self, rhs):
        return Complex(self.a*rhs.a-self.b*rhs.b,self.a*rhs.b+self.b*rhs.a)
     
    def __truediv__(self, rhs):
        a = self.a
        b = self.b
        c = rhs.a
        d = rhs.b
        return Complex((a*c+b*d)/(c*c+d*d),(-a*d+b*c)/(c*c+d*d))


t, a, b, c, d = [int(x) for x in input().split()]
c1 = Complex(a,b)
c2 = Complex(c,d)
if t == 1 : print(c1)
elif t == 2 : print(c2)
elif t == 3 : print(c1+c2)
elif t == 4 : print(c1*c2) 
else : print(c1/c2)
