#
# 05_List_12: 05_Nicknames 
#

name = ["Robert","William","James","John","Charles","Margaret","Edward","Sarah","Andrew","Anthony","Deborah","Cynthia"]
nick = ["Bob","Bill","Jim","Jack","Chuck","Peggy","Ed","Sally","Andy","Tony","Debbie","Cindy"]

n = int(input())

for i in range(n):
    s = input()
    if s in name: print(nick[name.index(s)])
    elif s in nick: print(name[nick.index(s)])
    else: print("Not found")