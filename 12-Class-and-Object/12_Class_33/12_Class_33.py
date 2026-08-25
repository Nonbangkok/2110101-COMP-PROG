#
# 12_Class_33: 12_Piggy-Bank-1 
#

class piggybank:
    def __init__(self):
        self.coins = {1:0,2:0,5:0,10:0}
        
    def add1(self, n):
        self.coins[1] += n
        
    def add2(self, n):
        self.coins[2] += n
        
    def add5(self, n):
        self.coins[5] += n
        
    def add10(self, n):
        self.coins[10] += n
        
    def __int__(self):
        return sum([i*j for i,j in self.coins.items()])
        
    def __lt__(self, rhs):
        return int(self) < int(rhs)
        
    def __str__(self):
        return str(self.coins).replace(': ',':')
        

cmd1 = input().split(';')
cmd2 = input().split(';')
p1 = piggybank(); p2 = piggybank()
for c in cmd1: eval(c)
for c in cmd2: eval(c)
