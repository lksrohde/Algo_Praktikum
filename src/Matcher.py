import os

import geopandas as geopd
import pandas as pd
from OSMPythonTools.nominatim import Nominatim

nom = Nominatim()

dataPath = os.path.dirname(__file__) + "/data/sensibleData"
timetables = dataPath + "/timetables/rohdaten/stamm/bfkoord.txt"
prognose = dataPath + "/prognose"
vg = dataPath + "/vg250/vg250_kompakt_3112/VG250_F.shp"

def handle_timetable():
    def read_timetable(path):
        return open(path, "r", encoding="iso-8859-1")

    fahrplan_file = read_timetable(timetables)
    fahrplan = fahrplan_file.readlines()

    for line in fahrplan:
        lineSplit = line.split(' ')
        lineSplit = [lineSplit[0], lineSplit[2], lineSplit[1]]
        # 0 -> AreaCode
        # 1 -> Longitude
        # 2 -> Latitude
        if lineSplit[0].startswith('0') or lineSplit[0].startswith('80'):

            location = nom.query(lineSplit[1], lineSplit[2], reverse=True, zoom=18)

            print(location.areaId())
            print(location.address())
            print(lineSplit[0])

def handle_landkreise():
    landkreise = geopd.read_file(vg)
    print(landkreise.describe())

handle_landkreise()
