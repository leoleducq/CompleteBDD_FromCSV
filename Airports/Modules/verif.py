#!/usr/bin/env python3.9


def LongLat(row):
    if len(row)>7 and "-"not in row:
        row = row[:7]
    if len(row)>8 and "-" in row:
        row= row[:8]
    return row

def VerifAltitude(altitude):
    if altitude =="":
        altitude = "0"
    return altitude
def VerifIata(icao,iata):
    if icao == iata:
        iata = ""
    return iata

def VerifInfoUrl(infourl):
    if "http" not in infourl:
        infourl = ""
    return infourl
