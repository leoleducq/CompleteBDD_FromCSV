#!/usr/bin/env python3.9
import datetime, os
from mysql.connector import Error
from Modules.exception import ErrorCSV, ErrorSQL
from Modules.verif import VerifAircrafts, VerifCallSign, VerifFirstRegDate, VerifIata, VerifIcaoExploitant, VerifIcaoTypeCode, VerifManufacturer, VerifModel, VerifOperator, VerifSerialnu, VerifSocair, VerifType, VerifTypeModel, VerifYearBuilt
from Modules.connect import Aircrafts_Connect, Socair_Connect
from Modules.unidecode import Unicode

startTime = datetime.datetime.now()
#---------------Réinitialise les fichiers Txt-----------------
#Fichier NewAircrafts
txt = open('Log/newaircrafts.txt',encoding='utf-8',mode='w')
txt.truncate()
txt.close()
#Fichier AircraftsExists
txt = open('Log/aircraftsexists.txt',encoding='utf-8',mode='w')
txt.truncate()
txt.close()
#Fichier NewSocair
txt = open('Log/newsocair.txt',encoding='utf-8',mode='w')
txt.truncate()
txt.close()
#Fichier SocairExists
txt = open('Log/socairexists.txt',encoding='utf-8',mode='w')
txt.truncate()
txt.close()
#Fichier ErrorSql
txt = open('Log/errorSql.txt',encoding='utf-8',mode='w')
txt.truncate()
txt.close
#Fichier ErrorCSV
txt = open('Log/errorCsv.txt',encoding='utf-8',mode='w')
txt.truncate()
txt.close

#Paramètres de connection BDD
aircrafts = Aircrafts_Connect()
socair = Socair_Connect()
#-----------------------------Connection BDD-----------------------------
try:
#Données de Fromaircrafts
    if aircrafts.is_connected():
        fromaircrafts_info = aircrafts.get_server_info()
        aircrafts_cursor = aircrafts.cursor()
        aircrafts_cursor.execute("Select Database();")
        rowloc = aircrafts_cursor.fetchone()

#Données de Socair
    if socair.is_connected():
        socair_info = socair.get_server_info()
        socair_cursor = socair.cursor()
        socair_cursor.execute("Select Database();")
        rowloc = socair_cursor.fetchone()
except Error as e:
    print("Erreur de connection à MySQL", e)

#-----------------------------Lecture du fichier-----------------------------
csv = open('Txt/aircraftDatabase.csv',encoding='utf-8',mode='r')
for lines in csv:
#Enlève les caractères à risques
    lines = Unicode(lines).replace('"','').replace("false","")
    newlines = lines.split(',')
#-------------------------------AIRCRAFTS-----------------------------
#Variables pour savoir si la clé primaire est vide
    boolaircrafts = True
    #ICAO
    try:
        icao = newlines[0].strip().upper()
    #Pour ignorer les 4 premières lignes
        if len(icao)!=6:
            continue
    #TYPE
        type = newlines[21].strip()
        type = VerifType(type)
    #COUNTRYICAO
        countryicao = ""
    #REGCODE
        regcode = newlines[1].strip().upper()
    #CATEGORIE
        categorie = ""
    #ICAOTYPECODE
        icaotypecode = newlines[8].strip().upper()
        icaotypecode = VerifIcaoTypeCode(icaotypecode)
    #MANUFACTURER
        manufacturer = newlines[3].strip().title()
        manufacturer = VerifManufacturer(manufacturer)
    #TYPEMODEl
        typemodel = newlines[5].strip().upper()
        typemodel = VerifTypeModel(typemodel)
    #MODEL
        model = newlines[4].strip()
        model = VerifModel(model)
    #SERIALNU
        serialnu = newlines[6].strip().upper()
        serialnu = VerifSerialnu(serialnu)
    #REGISTEREDOWENER
        registeredowener = newlines[13].strip()
    #ICAOOWENER #NBMOTEUR #TYPEMOTEUR #ICONNAME #TOTALHOURS
        icaoowener, nbmoteur, typemoteur, iconname, totalhours = "NULL", "0","","","NULL"
    #YEARBUILT
        yearbuilt = newlines[18].strip()
        yearbuilt = VerifYearBuilt(yearbuilt)
    #INFOURL #PICTUREURL #VIDEOURL #OPERATEURCODEFLAG #OWNERSHIPSTATUS
        infourl, pictureurl, videourl, operateurcodeflag, ownershipstatus = "NULL","NULL","NULL","NULL","NULL"
    #FIRSTREGDATE
        firstrgedate = newlines[16].strip()
        firstrgedate = VerifFirstRegDate(firstrgedate)
    #CURRENTREGDATE #DEREGDATE
        currentregdate, deregdate = "NULL","NULL"
    #STATUS
        status = newlines[17].strip()
    #UPDATED
        updated = "now()"
    #ICAOEXPLOITANT
        icaoexploitant = newlines[10].strip().upper()
        icaoexploitant = VerifIcaoExploitant(icaoexploitant)
    #ICAOPORTATTACHE #WAKETURBULENCE #SPECIES #MAJUSER #AFFPUBLIC #OWNEREMAIL #CODEPAYS
        icaoportattache, waketurbulence, species, majuser, affpublic, owneremail, codepays = "","0","","NULL","O","",""
    #Test de la clé primaire 
        boolaircrafts = VerifAircrafts(regcode)
    except:
        ErrorCSV(newlines)
#------------------Préparation de l'insertion dans AIRCRAFTS-----------------
#Dictionnaire contenant les valeurs à insérer
    if boolaircrafts== True:
        aircraftsdictionnary =''
        aircraftsdictionnary = '"'+icao+'","'+type+'","'+countryicao+'","'+regcode+'","'+categorie+'","'+icaotypecode+'","'+manufacturer+'","'+typemodel+'","'+model+'","'+serialnu+'",'
        aircraftsdictionnary += '"'+registeredowener+'","'+icaoowener+'",'+nbmoteur+',"'+typemoteur+'","'+iconname+'",'+totalhours+','+yearbuilt+','+infourl+','+pictureurl+','+videourl+','
        aircraftsdictionnary += operateurcodeflag+','+ownershipstatus+',"'+firstrgedate+'",'+currentregdate+','+deregdate+',"'+status+'",'+updated+',"'+icaoexploitant+'","'+icaoportattache+'",'
        aircraftsdictionnary += waketurbulence+',"'+species+'",'+majuser+',"'+affpublic+'","'+owneremail+'","'+codepays+'"'
        aircraftsdictionnary = str(aircraftsdictionnary).replace(',,',',"",').replace('"NULL"','NULL')
#-----------------------Requête SQL AIRCRAFTS-------------------------------------------
        insert_aircrafts = "INSERT INTO %s VALUES (%s)" % ("aircrafts", aircraftsdictionnary)
        insert_aircrafts = insert_aircrafts.replace("(,","(")
        print(insert_aircrafts)
        try:
            aircrafts_cursor.execute(insert_aircrafts)
            txt = open('Log/newaircrafts.txt','a')
            txt.write(insert_aircrafts+"\n")
            txt.close()
        except Error as e:
            #Erreur on DUPLICATE KEY
            if str(e.errno)=="1062":
                txt = open('Log/aircraftsexists.txt','a')
                txt.write(insert_aircrafts+"\n")
                txt.close()
            else:
                ErrorSQL(insert_aircrafts, e.msg)

#-------------------------------SOCAIR-----------------------------
#Variables pour savoir si la clé primaire est vide
    boolsocair = True
    try:
    #OPERATORIICAO
        operatoricao = newlines[11].strip()
        #CLE PRIMAIRE
        boolsocair = VerifSocair(operatoricao)
    #OPERATORIATA
        operatoriata = newlines[12].strip()
        operatoriata = VerifIata(operatoriata)
    #OPERATORCALLSIGN
        operatorcallsign = newlines[10].strip()
        operatorcallsign = VerifCallSign(operatorcallsign)
    #OPERATOR
        operator = newlines[9].strip()
        operator = VerifOperator(operator)
    except:
         ErrorCSV(newlines)
#---------------------Préparation de l'insertion dans SOCAIR-----------------
#Dictionnaire contenant les valeurs à insérer
    if boolsocair ==True:
        socairdictionnary =""
        socairdictionnary = '"'+operatoricao+'","'+operatoriata+'","'+operatorcallsign+'","'+operator+'","","","","",'+'NULL'+','+'NULL'+',""'
        socairdictionnary = str(socairdictionnary).replace(',,',',"",').replace("'NULL'","NULL")

#-----------------------Requête SQL SOCAIR----------------------------------------------
        insert_socair = "INSERT INTO %s VALUES (%s)" % ("socair", socairdictionnary)
        insert_socair = insert_socair.replace("(,","(")
        print(insert_socair)
        try:
            socair_cursor.execute(insert_socair)
            txt = open('Log/newsocair.txt','a')
            txt.write(insert_socair+"\n")
            txt.close()
        except Error as e:
        #Erreur on DUPLICATE KEY
            if str(e.errno)=="1062":
                txt = open('Log/socairexists.txt','a')
                txt.write(insert_socair+"\n")
                txt.close()
            else:
                ErrorSQL(insert_socair, e.msg)

#Permet d'insérer la dernière ligne
try:
    create_table = "CREATE TABLE ASUPPRIMER( asupprimer varchar (20))"
    aircrafts_cursor.execute(create_table)
    drop_table = "DROP TABLE ASUPPRIMER"
    aircrafts_cursor.execute(drop_table)
except Error as e:
    print(e.msg,e.errno)

#------------------Enlève les doublons des fichiers texte------------------
#AIRCRAFTS EXISTS
newdata = os.popen('sort Log/aircraftsexists.txt | uniq')
output = newdata.read()
txt = open('Log/aircraftsexists.txt',encoding='utf-8',mode='w')
txt.write(output)
txt.close()
#SOCAIR EXISTS
newdata = os.popen('sort Log/socairexists.txt | uniq')
output = newdata.read()
txt = open('Log/socairexists.txt',encoding='utf-8',mode='w')
txt.write(output)
txt.close()

#-----------------------Ferme toutes les connections-----------------------
if aircrafts.is_connected() and socair.is_connected():
#aircrafts
    aircrafts_cursor.close()
    aircrafts.close()
#socair
    socair_cursor.close()
    socair.close()
print(datetime.datetime.now()-startTime)