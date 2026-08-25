#
# 04_Loop_03: 04_MCQ 
#

a,b = input(),input()
print(
    sum(x == y for x,y in zip(a,b))
)