from OSMPythonTools.nominatim import Nominatim
import pandas as pd
import geopandas as geopd

nom = Nominatim()

def getData(path):
    return open(path, "r", encoding="iso-8859-1")    

file = getData("/Users/lukas/Documents/Uni/7.Semester/Algo_Praktikum/sensibleData/timetables/Data/rohdaten/stamm/bfkoord.txt")
lines = file.readlines()

for line in lines:
    lineSplitted = line.split(' ') 
    lineSplitted = [lineSplitted[0],lineSplitted[2],lineSplitted[1]]

    if (lineSplitted[0].startswith('0') or lineSplitted[0].startswith('80')):
        stelle = nom.query(lineSplitted[1], lineSplitted[2], reverse=True, zoom=18)
        
        print(stelle.areaId())
        print(stelle.address())
        print(lineSplitted[0])