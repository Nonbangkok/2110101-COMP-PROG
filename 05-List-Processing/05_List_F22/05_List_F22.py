#
# 05_List_F22: 05_Upgrade_2 (Function) 
#

def index_of(grades, ID):
    for i in range(len(grades)):
        if grades[i][0] == ID:
            return i
    return -1
    
    
def upgrade(grades, IDs):
    g = ['A','B+','B','C+','C','D+','D','F']
    for uid in IDs:
        if index_of(grades,uid) == -1 or grades[index_of(grades,uid)][1] == 'A': continue
        grades[index_of(grades,uid)][1] = g[g.index(grades[index_of(grades,uid)][1])-1]
    grades.sort()
    
# DON'T remove the following three lines
exec(input())
exec(input()) 
exec(input())