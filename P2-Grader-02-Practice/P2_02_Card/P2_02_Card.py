#
# P2_02_Card: Part-II-Card 
#


def f(x):
    return ('+' if x > 0 else '') + str(x)

def compare(a,b):
    value = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13}
    suit = {'C': 1, 'D': 2, 'H': 3, 'S': 4}
    if value[a[0]] != value[b[0]]: return value[a[0]] - value[b[0]]
    return suit[a[1]] - suit[b[1]]

s = input()
res = []

