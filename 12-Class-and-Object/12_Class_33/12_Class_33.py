#
# 12_Class_33: 12_Piggy-Bank-1 
#

class piggybank:
    def __init__(self):
        self.coin = {1:0,2:0,5:0,10:0}
        
    def add1(self, n):
        self.coin[1] += n
        
    def add2(self, n):
        self.coin[2] += n
        
    def add5(self, n):
        self.coin[5] += n
        
    def add10(self, n):
        self.coin[10] += n
        
    def __int__(self):
        return sum([i*j for i,j in self.coin.items()])
        
    def __lt__(self, rhs):
        return int(self) < int(rhs)
        
    def __str__(self):
        return str(self.coin).replace(': ',':')
