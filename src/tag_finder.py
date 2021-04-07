import csv
import json
import os

import geopandas as geopd
import pandas as pd
import shapely.geometry

import overpy

dataPath = os.path.dirname(__file__) + "/data"
timetables = dataPath + "/sensibleData/timetables/Data/rohdaten/stamm"
prognose = dataPath + "/sensibleData/verkehrsverflechtungsprognose/PVMatrix_BVWP15_P2030/PVMatrix_BVWP15_P2030.csv"
vg = dataPath + "/sensibleData/vg250/vg250_kompakt_3112/VG250_F.shp"

verkehrszellen_mapping = dataPath + "/sensibleData/verkehrsverflechtungsprognose/PVMatrix_BVWP15_P2030/Verkehrszellen_BVWP15.xlsx"
json_haltestellen = timetables + "/newData/haltestellen"
aggregated_nuts_regions = dataPath + "/nuts.geojson/aggregated_nuts_regions.json"


def read_timetable(path):
    return open(path, "r", encoding="iso-8859-1")

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return float('.'.join([i, (d+'0'*n)[:n]]))
'''
Matches DB Haltestelle mit den Regionen der Verkehrsverflechtungsprognose
'''
def match_kreis_haltestelle_simplified():
    aggregated_nuts_json = open(aggregated_nuts_regions, "r")
    aggregated_nuts_data = json.load(aggregated_nuts_json)

    de_path = dataPath + "/landkreise_simplify0.geojson"
    de_geo_json = geopd.read_file(de_path)

    nuts_path = "/Users/lukas/Documents/Uni/7.Semester/Algo_Praktikum/src/data/exact_nuts.geojson/NUTS_RG_01M_2010_4326.geojson"
    nuts_geo_json = geopd.read_file(nuts_path)

    # Koordinaten der Haltestellen
    haltestellen_data = read_timetable(timetables + "/bfkoord.txt")

    # Zuordnung Kreisname auf KKZ
    #excel_file = open(verkehrszellen_mapping, "r", encoding="iso-8859-1")
    prognose_map_data_de = pd.read_excel(verkehrszellen_mapping, "ME1_D_AKS", engine="openpyxl")
    prognose_map_data_rest = pd.read_excel(verkehrszellen_mapping, "ME1_Ausland", engine="openpyxl")

    output_file = open(json_haltestellen + "_mapped.json", "w")
    levl_codes = {
        "0": [
            "N", "FIN", "EE", "LV", "LT", "RU2", "RU1", "BY", "UA", "MD", "RO", "BG", "TR",
            "GR", "MK", "AL", "XK", "ME", "SRB", "BIH", "HR", "SL", "ES", "PT", "IRL"
        ]
    }

    osm_tags = {
        "Fz1": [
            '"landuse"="commercial"', '"building"="commercial"', '"building"="industrial"', '"building"="office"'
        ],
        "Fz2": [
            '"amenity"="college"', '"amenity"="school"', '"amenity"="university"'
        ],
        "Home": [
            '"building"="apartments"', '"building"="bungalow"', '"building"="cabin"',
            '"building"="detached"', '"building"="dormitory"', '"building"="house"', '"building"="residential"'
        ]
    }

    def build_query(tag):
        query = "[out:json][timeout:600]; ("
        for string in osm_tags[tag]:
            query = query + "relation[" + string + "]({{bbox}}); "
        query = query + "); out center;"

        return query

    def handle_region(line_split):
        lon = float(line_split[1])
        lat = float(line_split[2])

        # If not found anything use broader coords
        for i in range(8,0, -1):
            lon = truncate(lon, i)
            lat = truncate(lat, i)

            coords = shapely.geometry.Point(lat, lon)

            print("Current Point: ", coords)


            # Handle Germany
            for i, kreis in enumerate(de_geo_json['geometry']):

                # osm_region = pyrosm.pyrosm.OSM("europe-latest.osm.pbf", kreis)


                ''' 
                if kreis.contains(coords):
                    print(line_split[0], coords, de_geo_json['GEN'][i], de_geo_json['AGS'][i])
                    return line_split[0], coords, de_geo_json['GEN'][i], de_geo_json['AGS'][i]
                '''
            print("Deutschland gecheckt!")

            #Handle Nuts
            for i, nuts in enumerate(nuts_geo_json.get('geometry')):
                if nuts.contains(coords):

                    name = nuts_geo_json['NUTS_NAME'][i]
                    id = nuts_geo_json['NUTS_ID'][i]
                    code = nuts_geo_json["LEVL_CODE"][i]

                    if not (id in levl_codes["0"]) and code == 0:
                        continue

                    print("gefunden", name, id)

                    for j, prognose in enumerate(prognose_map_data_rest['Bezeichnung_ME1']):
                        if name in prognose:
                            print(line_split[0], coords, name, prognose_map_data_rest['Nr_ME1'][j], "Nuts")
                            return line_split[0], coords, name, prognose_map_data_rest['Nr_ME1'][j]

                    for aggregated in aggregated_nuts_data:
                        if id in aggregated_nuts_data[aggregated]['regions']:
                            print(line_split[0], coords, name, aggregated, "Agg. Nuts")
                            return line_split[0], coords, name, aggregated

            print("Going Broader")

    csv_file = open('file_mapping.csv', 'w')
    csv_writer = csv.writer(csv_file)
    header = ['db_ip', 'point', 'region', 'vp_ip']
    csv_writer.writerow(header)

    for line in haltestellen_data:
        line_split = line.split(' ')
        # 0 -> AreaCode     # 1 -> Longitude    # 2 -> Latitude
        line_split = [line_split[0], line_split[2], line_split[1]]

        # Bus und Bahn Verkehr
        if line_split[0].startswith('0') or line_split[0].startswith('80'):

            db_ip, point, region, vp_ip = handle_region(line_split)

            csv_writer.writerow([db_ip, point, region, vp_ip])





match_kreis_haltestelle_simplified()