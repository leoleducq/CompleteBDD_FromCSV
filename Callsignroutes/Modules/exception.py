#!/usr/bin/env python3.9

#Gestion des erreurs de Socair
def MissingSocair(missingsocair):
    if len(missingsocair)!= 3 or missingsocair =="NULL":
        pass
    else:
        print("Données manquantes dans la table Socair")
        data = "Code ICAO de l'opérateur manquant : %s" % (missingsocair)
        txt = open('Error/missingSocair.txt',encoding='utf-8',mode='a')
        txt.write(data+"\n")
        txt.close()

#Gestion des erreurs de Airports
def MissingAirports(missingairport):
    if len(missingairport) !=4 or any(word in missingairport for word in("?","-","*","/","#")):
        pass
    else: 
        print("Données manquantes dans la table Airports")
        data = "Code ICAO de l'aéroport manquant : %s" % (missingairport)
        txt = open('Error/missingAirports.txt',encoding='utf-8',mode='a')
        txt.write(data+"\n")
        txt.close()

#Gestion des erreurs de requêtes SQL
def ErrorSQL(errorsql, errormsg):
    print("Erreur dans une des requêtes SQL")
    txt = open('Error/errorSql.txt',encoding='utf-8',mode='a')
    txt.write(str(errorsql)+str(errormsg)+"\n")
    txt.close()

#Gestion des erreurs de data
def ErrorData(errordata):
    print("Erreur dans une des requêtes SQL")
    test = "callsign : %s | operatoricao : %s | fromairporticao : %s | toairporticao : %s " % (errordata[0], errordata[1],errordata[2],errordata[4])
    txt = open('Error/errorData.txt',encoding='utf-8',mode='a')
    txt.write(str(test)+"\n")
    txt.close()