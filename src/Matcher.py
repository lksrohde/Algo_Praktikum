from OSMPythonTools.nominatim import Nominatim
import pandas as pd
import geopandas as geopd

nom = Nominatim()


def get_data(path):
    return open(path, "r", encoding="iso-8859-1")


file = get_data(
    "/Users/lukas/Documents/Uni/7.Semester/Algo_Praktikum/sensibleData/timetables/Data/rohdaten/stamm/bfkoord.txt")
lines = file.readlines()

for line in lines:
    lineSplit = line.split(' ')
    lineSplit = [lineSplit[0], lineSplit[2], lineSplit[1]]

    if lineSplit[0].startswith('0') or lineSplit[0].startswith('80'):
        location = nom.query(lineSplit[1], lineSplit[2], reverse=True, zoom=18)

        print(location.areaId())
        print(location.address())
        print(lineSplit[0])
