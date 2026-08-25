#
# 10_TSD_37: 10_Dept Selection 
#

def get_major(nums,student):
    for i in range(2,6):
         if nums[student[i]]:
              nums[student[i]] -= 1
              return student[i]

n = int(input())
nums = {}

for i in range(n):
    a = input().split()
    nums[a[0]] = int(a[1])

m = int(input())
students = []
for i in range(m):
    students.append(input().split())
students.sort(key=lambda x: -float(x[1]))

res = []
for i in range(m):
    res.append([students[i][0],get_major(nums,students[i])])

print("\n".join(" ".join(s) for s in sorted(res)))