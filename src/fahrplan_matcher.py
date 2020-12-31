import os

import geopandas as geopd
import geoplot as geoplt
import geoplot.crs as gcrs
import matplotlib.pyplot as plt
import pandas as pd
from OSMPythonTools.nominatim import Nominatim
from shapely.geometry import Point, Polygon

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
        line_split = line.split(' ')
        line_split = [line_split[0], line_split[2], line_split[1]]
        # 0 -> AreaCode
        # 1 -> Longitude
        # 2 -> Latitude
        if line_split[0].startswith('0') or line_split[0].startswith('80'):

            location = nom.query(line_split[1], line_split[2], reverse=True, zoom=18)
            point = Point(float(line_split[2]), float(line_split[1]))
            get_verwaltungsbezirk(point)
            #print(location.areaId())
            print(location.address())
            #print(line_split[0])

def get_verwaltungsbezirk(haltestelle):
    vw_bezirke = geopd.read_file(vg)
    
    temp0 = {'ARS': [vw_bezirke.get("ARS")[11151]], 'geometry': vw_bezirke.get("geometry")[11151]}
    gdf = geopd.GeoDataFrame(temp0)
    print(gdf)
    #geoplt.polyplot(vw_bezirke)
    gdf.plot()
    plt.show()
    vw_bezirke.plot()
    plt.show()    
    #print(haltestelle.within(vw_bezirke))   

#handle_timetable()
get_verwaltungsbezirk(1)
