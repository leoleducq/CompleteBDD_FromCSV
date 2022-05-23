#!/usr/bin/env python3.9
def VerifIata(icao,iata):
    if icao == iata:
        iata = ""
    return iata

def VerifInfoUrl(infourl):
    if "http" not in infourl:
        infourl = ""
    return infourl
#------------------Verif Aircrafts-----------------------
#PRIMARYKEY
def VerifAircrafts(regcode):
    if (regcode=="") or ("(" in regcode) or (len(regcode)>8):
        boolaircrafts = False
    return boolaircrafts

#TYPE
def VerifType(type):
    if len(type)>8:
        type=""
    return type
#YEARBUILT
def VerifYearBuilt(yearbuilt):
    if yearbuilt=="":
        yearbuilt="NULL"
    return yearbuilt

#FIRSTREGDATE
def VerifFirstRegDate(firstregdate):
    #Ne prend que l'année
    firstregdate = firstregdate[:4]
    if firstregdate =="" or not firstregdate.isnumeric():
        firstregdate ="NULL"
    return firstregdate

#SERIALNU
def VerifSerialnu(serialnu):
    if len(serialnu) >10:
        serialnu=""
    return serialnu

#ICAOEXPLOITANT
def VerifIcaoExploitant(icaoexploitant):
    icaoexploitant = icaoexploitant[:10]
    return icaoexploitant

#ICAOTYPECODE
def VerifIcaoTypeCode(icaotypecode):
    icaotypecode = icaotypecode[:3]
    return icaotypecode
#MODEL
def VerifModel(model):
    model = model[:50]
    return model

#MANUFACTURER
def VerifManufacturer(manufacturer):
    manufacturer = manufacturer[:100]
    return manufacturer

#TYPEMODEL
def VerifTypeModel(typemodel):
    typemodel = typemodel[0:50]
    return typemodel
#------------------Verif Socair-----------------------
#PRIMARYKEY
def VerifSocair(operatoricao):
    if (operatoricao=="") or ("(" in operatoricao) or (len(operatoricao)>3):
        boolsocair = False
    return boolsocair

#OPERATORCALLSIGN
def VerifCallSign(callsign):
    #Len callsign <= 10
    callsign = callsign[:10]
    return callsign

#IATA
def VerifIata(operatoriata):
    operatoriata = operatoriata[:2]
    return operatoriata
#OPERATOR
def VerifOperator(operator):
    operator = operator[:50]
    return operator