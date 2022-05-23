#!/usr/bin/env python3.9
import unidecode
def Unicode(newrow):
    #Enleve les accents et les espaces et met la chaine en MAJUSCULE
    newrow = str(unidecode.unidecode(newrow)).upper()
    return newrow