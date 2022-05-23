#!/usr/bin/env python3.9
import mysql.connector

BDD = mysql.connector.connect(
        host="127.0.0.1",
        port ="3306",
        database ="completeBDD",
        user="leo",
        password="leoadsbnetwork"
)
#--------------Données de Aircrafts----------------
def Aircrafts_Connect():
    #Paramètres BDD sur laquelle coller
    fromAirports = BDD
    return fromAirports

#--------------Données de Socair----------------
def Socair_Connect():
    #Paramètres BDD sur laquelle coller
    socair = BDD
    return socair