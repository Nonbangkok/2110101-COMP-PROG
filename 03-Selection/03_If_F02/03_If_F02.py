#
# 03_If_F02: 03_Change_of_Major (Function) 
#

def choose(stu1, stu2):
    pass1 = []

    if(stu1[2] == 'A' and ord(stu1[3])-65 <= 2 and ord(stu1[4])-65 <= 2):
        pass1.append(stu1)
    if(stu2[2] == 'A' and ord(stu2[3])-65 <= 2 and ord(stu2[4])-65 <= 2):
        pass1.append(stu2)

    if len(pass1) == 0:
        return []
    elif len(pass1) == 1:
        return [pass1[0][0]]
    else:
        winner = []
        if stu1[1] > stu2[1]: winner.append(stu1)
        elif stu1[1] < stu2[1]: winner.append(stu2)
        else:
            if ord(stu1[3]) < ord(stu2[3]): winner.append(stu1)
            elif ord(stu1[3]) > ord(stu2[3]): winner.append(stu2)
            else:
                if ord(stu1[4]) < ord(stu2[4]): winner.append(stu1)
                elif ord(stu1[4]) > ord(stu2[4]): winner.append(stu2)
        if len(winner) == 0:
            return [pass1[0][0],pass1[1][0]]
        else:
            return [winner[0][0]]
    