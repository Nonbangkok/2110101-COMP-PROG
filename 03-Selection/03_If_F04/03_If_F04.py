#
# 03_If_F04: 03_MobileNumber (Function) 
#

def is_mobile_number(number):
    prefix = ["06","08","09"]
    return True if len(number) == 10 and number[:2] in prefix else False 
    