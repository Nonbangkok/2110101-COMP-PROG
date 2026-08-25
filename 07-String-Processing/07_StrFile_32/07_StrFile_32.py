#
# 07_StrFile_32: 07_Password_Strength 
#

def no_lowercase(t): # return True if no lowercase, otherwise return False
    return not any(c.islower() for c in t)
    
def no_uppercase(t):
    return not any(c.isupper() for c in t)
    
def no_number(t):
    return not any(c.isdigit() for c in t)
    
def no_symbol(t):
    return all(c.isalnum() for c in t)
    
def character_repetition(t):
    for i in range(len(t)-3):
        if t[i]==t[i+1]==t[i+2]==t[i+3]:
            return True
    return False

def check_sequence(t,seq,n):
    for i in range(len(t)-n+1):
        if t[i:i+n].lower() in seq:
            return True
    return False
    
def number_sequence(t):
    seq = '01234567890'
    if check_sequence(t,seq,4):
        return True
    return check_sequence(t,seq[::-1],4)
    
def letter_sequence(t):
    seq = 'abcdefghijklmnopqrstuvwxyz'
    if check_sequence(t,seq,4):
        return True
    return check_sequence(t,seq[::-1],4)
    
def keyboard_pattern(t):
    seq = '!@#$%^&*()_+\nqwertyuiop\nasdfghjkl\nzxcvbnm'
    if check_sequence(t,seq,4):
        return True
    return check_sequence(t,seq[::-1],4)
 
#-----------------------------
