#
# 01_Expr_02: 01_Quadratic_Root 
#

a = float(input())
b = float(input())
c = float(input())

sq = (b*b-4*a*c)**0.5
print(round((-b-sq)/2/a,3),round((-b+sq)/2/a,3))