#
# 07_StrFile_33: 07_File_Merge 
#

fn1,fn2 = input().split()
lines = open(fn1).read().splitlines() + open(fn2).read().splitlines()
students = [line.split() for line in lines if line.strip()]
students.sort(key=lambda x: (x[0][-2:],x[0]))
print("\n".join(" ".join([i,j]) for i,j in students))