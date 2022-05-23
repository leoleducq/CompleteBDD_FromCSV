#!/usr/bin/env python3.9
import mysql.connector

#--------------Données de FromAirports----------------
BDD = mysql.connector.connect(
        host="127.0.0.1",
        port ="3306",
        database ="completeBDD",
        user="leo",
        password="leoadsbnetwork"
)
def FromAirports_Connect():
    #Paramètres BDD sur laquelle coller
    fromAirports = BDD
    return fromAirports

#--------------Données de FromAirports----------------

def ToAirports_Connect():
    #Paramètres BDD sur laquelle coller
    toAirports = BDD
    return toAirports

#--------------Données de Callsign----------------
def Callsignroutes_Connect():
    #Paramètres BDD sur laquelle coller
    callsignroutes = BDD
    return callsignroutes

#--------------Données de Socair----------------
def Socair_Connect():
    #Paramètres BDD sur laquelle coller
    socair = BDD
    return socair