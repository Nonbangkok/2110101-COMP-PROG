#
# 12_Class_23: 12_Next-Card 
#

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        
    def __str__(self):
        return f"({self.value} {self.suit})"
        
    def next1(self):
        order_value = ['3','4','5','6','7','8','9','10','J','Q','K','A','2']
        order_suit = ['club','diamond','heart','spade']
        if self.value == '2' and self.suit == 'spade': return Card('3','club')
        if self.suit != 'spade': return Card(self.value,order_suit[order_suit.index(self.suit)+1])
        return Card(order_value[order_value.index(self.value)+1],'club')
        
    def next2(self):
        next = self.next1()
        self.value = next.value
        self.suit = next.suit