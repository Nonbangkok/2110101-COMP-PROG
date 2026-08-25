#
# 04_Loop_F03: 04_MCQ (Function) 
#

def grade_mcq(sol, ans):
    return sum(a == b for a,b in zip(sol,ans)) if len(sol) == len(ans) else -1