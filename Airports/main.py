#!/usr/bin/env python3.9
import datetime
from mysql.connector import Error
from Modules.exception import ErrorSQL
from Modules.verif import LongLat, VerifAltitude, VerifIata, VerifInfoUrl
from Modules.connect import Airports_Connect
from Modules.unidecode import Unicode

startTime = datetime.datetime.now()
#---------------Réinitialise les fichiers Txt-----------------
#Fichier NewAirports
txt = open('Log/newAirports.txt',encoding='utf-8',mode='w')
txt.truncate()
txt.close()
#Fichier ErrorSql
txt = open('Log/errorSql.txt',encoding='utf-8',mode='w')
txt.truncate()
txt.close
#Paramètres de connection BDD
airports = Airports_Connect()
#-----------------------------Connection BDD-----------------------------
try:
#Données de FromAirports
    if airports.is_connected():
        fromAirports_info = airports.get_server_info()
        airports_cursor = airports.cursor()
        airports_cursor.execute("Select Database();")
        rowloc = airports_cursor.fetchone()
except Error as e:
    print("Erreur de connection à MySQL", e)

#-----------------------------Lecture du fichier-----------------------------
csv = open('Txt/airports.csv',encoding='utf-8',mode='r')
for lines in csv:
#Enlève les caractères à risques
    lines = Unicode(lines).replace('"',"")
    newlines = lines.split(',')

#ICAO
    icao = newlines[1].strip().upper()
    #Pour ignorer la 1ère ligne
    if len(icao)>4:
        continue
#IATA
    iata = newlines[14].strip()
    iata = VerifIata(icao,iata)
#AIRPORT
    airport = newlines[3].strip()
#VILLE
    ville = newlines[10].strip()
#LATITUDE
    latitude = newlines[4].strip()
    latitude = LongLat(latitude)
#LONGITUDE
    longitude = newlines[5].strip()
    longitude = LongLat(longitude)
#ALTITUDE
    altitude = newlines[6].strip()
    altitude = VerifAltitude(altitude)
#PAYS
    pays = newlines[8].strip()
#GMTOFFSET
    gmtoffset = "0"
#DSTOFFSET
    dstoffset ="0"
#CONTINENT
    continent = newlines[7].strip()
#TYPE
    type = newlines[2].strip().title()
#INFOURL
    infourl = newlines[15].strip()
    infourl = VerifInfoUrl(infourl)
#CODEDST
    codedst = ""
#TIMEZONE
    timezone =""
#----------------------------------Requête-----------------------------------
#Requête de Airports
    airports_select = "SELECT * FROM airports WHERE icao = '%s'" % (icao)
#-------------------------Execute toutes les requêtes------------------------
#Airports
    try:
        airports_cursor.execute(airports_select)
        data = airports_cursor.fetchone()
    except Error as e:
        ErrorSQL(newlines, e.msg)
        continue
    #Si l'aéroport est déjà dans la BDD -> Suivant
    if data is not None:
        continue
#------------Préparation de l'insertion dans airports-----------------

#Dictionnaire contenant les valeurs à insérer
    dictionnaryvalues =""
    dictionnaryvalues = '"'+iata+'","'+icao+'","'+airport+'","'+ville+'",'+latitude+','+longitude+','+altitude+',"'+pays+'",'+gmtoffset+','+dstoffset+',"'+continent+'","'+type+'","'+infourl+'",'+codedst+',"'+timezone+'"'
    dictionnaryvalues = str(dictionnaryvalues).replace(',,',',"",')

#-----------------------Requête SQL airports-----------------------
    insert_data = "INSERT INTO %s VALUES (%s)" % ("airports", dictionnaryvalues)
    insert_data = insert_data.replace("(,","(")
    print(insert_data)
    try:
       airports_cursor.execute(insert_data)
       txt = open('Log/newAirports.txt','a')
       txt.write(insert_data+"\n")
       txt.close()
    except Error as e:
        #Erreur on DUPLICATE KEY
        if str(e.errno)=="1062":
            continue
        else:
            ErrorSQL(insert_data, e.msg)
            continue

#Permet d'insérer la dernière ligne
create_table = "CREATE TABLE ASUPPRIMER( asupprimer varchar (20))"
airports_cursor.execute(create_table)
drop_table = "DROP TABLE ASUPPRIMER"
airports_cursor.execute(drop_table)

#------------------Enlève les doublons des fichiers texte------------------

#-----------------------Ferme toutes les connections-----------------------
if airports.is_connected():
#Airports
    airports_cursor.close()
    airports.close()
print(datetime.datetime.now()-startTime)