#
# 01_Expr_07: 01_Body_Surface_Area (Function) 
#

import math

def mosteller(w, h):
    return ((w*h)**0.5)/60

def du_bois(w, h):
    return 0.007184 * (w**0.425) * (h**0.725)

def fujimoto(w, h):
    return 0.008883 * (w**0.444) * (h**0.663)

def main():
    weight = float(input())
    height = float(input())
    
    M = mosteller(weight,height)
    D = du_bois(weight,height)
    F = fujimoto(weight,height)
    
    print("Mosteller =", round(M, 5))
    print("Du Bois =", round(D, 5))
    print("Fujimoto =", round(F,5))
    

