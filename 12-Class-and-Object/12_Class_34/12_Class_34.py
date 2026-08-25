#
# 12_Class_34: 12_Piggy-Bank-2 
#

class piggybank:
    def __init__(self):
        self.coins = {}
        self.nums = 0
        
    def add(self, v, n):
        if self.nums + n > 100: return False
        self.nums += n
        v = float(v)
        self.coins[v] = self.coins.get(v,0) + n
        return True
        
    def __float__(self):
        return float(sum([i*j for i,j in self.coins.items()]))
        
    def __str__(self):
        return str(dict(sorted(self.coins.items()))).replace(': ',':')
