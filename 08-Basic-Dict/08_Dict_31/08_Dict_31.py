#
# 08_Dict_31: 08_Cash 
#

def total(pocket):
    return sum(a*b for a,b in pocket.items())
    
def take(pocket, money_in):
    for value,number in money_in.items():
        pocket[value] = pocket.get(value,0) + number
 
def pay(pocket, amt):
    paid = {}
    for value,number in sorted(pocket.items(),reverse=True):
        if value > amt: continue
        coin = min(amt//value,number)
        amt -= coin * value
        paid[value] = coin
        pocket[value] -= coin
        
    if amt:
        for value,number in paid.items():
            pocket[value] += number
        return {}
    return paid  
