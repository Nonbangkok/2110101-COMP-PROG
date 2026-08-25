#
# 12_Class_22: 12_Card 
#

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        
    def __str__(self):
        return f"({self.value} {self.suit})"
        
    def getScore(self):
        if self.value == 'A': return 1
        elif self.value in 'JQK': return 10
        return int(self.value)
        
    def sum(self, other):
        return (self.getScore()+other.getScore()) % 10
        
    def __lt__(self, rhs):
        order_value = ['3','4','5','6','7','8','9','10','J','Q','K','A','2']
        order_suit = ['club','diamond','heart','spade']
        if(self.value != rhs.value): return order_value.index(self.value) < order_value.index(rhs.value)
        return order_suit.index(self.suit) < order_suit.index(rhs.suit)
        
n = int(input())
cards = []
for i in range(n):
    value, suit = input().split()
    cards.append(Card(value, suit))
for i in range(n):
    print(cards[i].getScore())
print("----------")
for i in range(n-1):
    print(Card.sum(cards[i], cards[i+1]))
print("----------")
cards.sort()
for i in range(n):
    print(cards[i])
