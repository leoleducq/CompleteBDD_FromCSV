#!/usr/bin/env python3.9
import datetime, os, re
from mysql.connector import Error
from Modules.exception import ErrorSQL, ErrorData, MissingSocair, MissingAirports
from Modules.verif import Verif
from Modules.connect import Callsignroutes_Connect, FromAirports_Connect, Socair_Connect, ToAirports_Connect
from Modules.unidecode import Unicode

startTime = datetime.datetime.now()
#---------------Réinitialise les fichiers Error-----------------
#Fichier Airports
txt = open('Error/missingAirports.txt',encoding='utf-8',mode='w')
txt.truncate()
txt.close()
#Fichier Socair
txt = open('Error/missingSocair.txt',encoding='utf-8',mode='w')
txt.truncate()
txt.close()
#Fichier ErrorSql
txt = open('Error/errorSql.txt',encoding='utf-8',mode='w')
txt.truncate()
txt.close
#Fichier ErrorData
txt = open('Error/errorData.txt',encoding='utf-8',mode='w')
txt.truncate()
txt.close
#Paramètres de connection BDD
fromAirports = FromAirports_Connect()
toAirports = ToAirports_Connect()
callsignroutes = Callsignroutes_Connect()
socair = Socair_Connect()
#-----------------------------Connection BDD-----------------------------
try:
#Données de FromAirports
    if fromAirports.is_connected():
        fromAirports_info = fromAirports.get_server_info()
        fromAirports_cursor = fromAirports.cursor()
        fromAirports_cursor.execute("Select Database();")
        rowloc = fromAirports_cursor.fetchone()
#Données de ToAirports
    if toAirports.is_connected():
        toAirports_info = toAirports.get_server_info()
        toAirports_cursor = toAirports.cursor()
        toAirports_cursor.execute("Select Database();")
        rowloc = toAirports_cursor.fetchone()
#Données de Callsign
    if callsignroutes.is_connected():
        callsignroutes_info = callsignroutes.get_server_info()
        callsignroutes_cursor = callsignroutes.cursor()
        callsignroutes_cursor.execute("Select Database();")
        rowloc = callsignroutes_cursor.fetchone()
#Données de Socair
    if socair.is_connected():
        socair_info = socair.get_server_info()
        socair_cursor = socair.cursor()
        socair_cursor.execute("Select Database();")
        rowloc = socair_cursor.fetchone()
except Error as e:
    print("Erreur de connection à MySQL", e)

#-----------------------------Lecture du fichier-----------------------------
csv = open('Txt/routes.tsv','r')
for lines in csv:
#Enlève les caractères à risques
    lines = Unicode(lines)
    newlines = lines.split('\t')
#Prend le callsign dans callsignroutes
    callsign = newlines[0].strip()
#Prend l'icao de l'opérateur dans callsignroutes
    operatoricao = newlines[1].strip()
    #Enlève les numéros
    operatoricao = re.sub("\d+","", operatoricao)
#Prend l'icao de FromAirport dans airports
    fromairporticao = newlines[2].strip()
    fromairporticao = re.sub("\d+","", fromairporticao)
#Prend l'icao de ToAirport dans airports
    toairporticao = newlines[4].strip()
    toairporticao = re.sub("\d+","", toairporticao)

#----------------------------------Requête-----------------------------------
#Requête de FromAirports
    fromairports_select = "SELECT icao,iata, airport, latitude, longitude, altitude, ville, pays FROM airports WHERE icao = '%s'" % (fromairporticao)
#Requête de ToAirports
    toairports_select = "SELECT icao,iata, airport, latitude, longitude, altitude, ville, pays FROM airports WHERE icao = '%s'" % (toairporticao)
#Requête de Socair
    socair_select = "SELECT iata,designation FROM socair WHERE icao = '%s'" % (operatoricao)
    try:
#----------------Execute toutes les requêtes--------------------
#FromAirports
        fromAirports_cursor.execute(fromairports_select)
        fromdata = fromAirports_cursor.fetchone()
#ToAirports
        toAirports_cursor.execute(toairports_select)
        todata = toAirports_cursor.fetchone()
#Socair
        socair_cursor.execute(socair_select)
        socairdata = socair_cursor.fetchone()
    except Error as e:
        ErrorSQL(newlines, e.msg)
        continue
#-----------Test si une des requêtes est vide-----------
#From Airports
    try:
        emptyfrom = fromdata[0]
    except:
        MissingAirports(fromairporticao)
        continue
#To Airports    
    try:
        emptyto = todata[0]
    except:
        MissingAirports(toairporticao)
        continue
#Table Socair
    try:
        emptysocair = socairdata[0]
    except:
        MissingSocair(operatoricao)
        continue
#Vérification des champs
    verif = Verif(callsign,fromairporticao,toairporticao,operatoricao)
    if verif != True:
        ErrorData(newlines)
        continue
#------------Préparation de l'insertion dans callsignroutes-----------------
    routeicao = fromdata[0]+"-"+todata[0]
    routeiata = fromdata[1]+"-"+todata[1]
#Socair iata
    operatoriata = socairdata[0]
#Socair designation
    operatorname = socairdata[1]
    flightnumber = callsign.replace(operatoricao,operatoriata)
#Dictionnaire contenant les valeurs à insérer
    dictionnaryvalues =""
    dictionnaryvalues = "'"+callsign +"','"+ routeicao +"','"+ routeiata +"','"+ operatoricao +"','"+operatoriata+"','"+ operatorname +"','"+ flightnumber +"',"+ str(fromdata) +","+ str(todata) + ",'"+"0"+"','"+"0"+"',"+"now()"+","+"''"
    dictionnaryvalues = str(dictionnaryvalues).replace("(","").replace(")","").replace("now","now()")

#-----------------------Requête SQL callsignroutes-----------------------
    insert_data = "INSERT INTO %s VALUES (%s)" % ("callsignsroutes", dictionnaryvalues)
    print(insert_data)
    try:
        callsignroutes_cursor.execute(insert_data)
    except Error as e:
        #Erreur on DUPLICATE KEY
        if str(e.errno)=="1062":
            continue
        else:
            ErrorSQL(insert_data, e.msg)
            continue

#Permet d'insérer la dernière ligne
create_table = "CREATE TABLE ASUPPRIMER( asupprimer varchar (20))"
callsignroutes_cursor.execute(create_table)
drop_table = "DROP TABLE ASUPPRIMER"
callsignroutes_cursor.execute(drop_table)

#------------------Enlève les doublons des fichiers texte------------------
#MISSING AIPORTS
newdata = os.popen('sort Error/missingAirports.txt | uniq')
output = newdata.read()
txt = open('Error/missingAirports.txt',encoding='utf-8',mode='w')
txt.write(output)
txt.close()
#MISSING SOCAIR
newdata = os.popen('sort Error/missingSocair.txt | uniq')
output = newdata.read()
txt = open('Error/missingSocair.txt',encoding='utf-8',mode='w')
txt.write(output)
txt.close()

#-----------------------Ferme toutes les connections-----------------------
if fromAirports.is_connected() and toAirports.is_connected() and callsignroutes.is_connected():
#fromAirports
    fromAirports_cursor.close()
    fromAirports.close()
#toAirports
    toAirports_cursor.close()
    toAirports.close()
#callsignroutes
    callsignroutes_cursor.close()
    callsignroutes.close()
print(datetime.datetime.now()-startTime)