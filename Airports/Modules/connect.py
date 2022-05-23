#!/usr/bin/env python3.9
import mysql.connector

#--------------Données de Airports----------------

def Airports_Connect():
    #Paramètres BDD sur laquelle coller
    Airports = mysql.connector.connect(
        host="127.0.0.1",
        port ="3306",
        database ="completeBDD",
        user="leo",
        password="leoadsbnetwork"
    )
    return Airports
