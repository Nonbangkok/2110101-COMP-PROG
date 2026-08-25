#
# 04_Loop_01: 04_Average 
#

d = [float(n) for n in iter(input, 'q')]
print(round(sum(d) / len(d), 2) if d else "No Data")
