#
# 07_StrFile_23: 07_File_Min_Max_Average 
#

try:
    filename, year = input().split()
    target = str(int(year) - 2500)
    scores = [float(line.split()[1]) for line in open(filename) if line.split()[0].startswith(target)]
    print(f"{min(scores)} {max(scores)} {sum(scores)/len(scores)}")
except:
    print("No data")
