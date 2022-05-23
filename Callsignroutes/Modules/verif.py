#!/usr/bin/env python3.9

def Verif(callsign,fromairporticao,toairporticao,operatoricao):
    verif = True
    
    if callsign[:3] != operatoricao:
        verif = False
    elif len(fromairporticao) !=4 or len(toairporticao) != 4:
        verif = False

    return verif