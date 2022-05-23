#!/usr/bin/env python3.9

#Gestion des erreurs de requêtes SQL
def ErrorSQL(errorsql, errormsg):
    txt = open('Log/errorSql.txt',encoding='utf-8',mode='a')
    txt.write(str(errorsql)+str(errormsg)+"\n")
    txt.close()

def ErrorCSV(newlines):
    txt = open('Log/errorCsv.txt',encoding='utf-8',mode='a')
    txt.write(str(newlines)+"\n")
    txt.close()