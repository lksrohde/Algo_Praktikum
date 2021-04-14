import csv
import json
import shapely.geometry
import geopandas as geopd

# Notwendig um die aggregierten NUTS Regionen der Prognose zu finden
aggregated_nuts_json = open("necessary_files/aggregated_nuts_regions.json", "r")
aggregated_nuts_data = json.load(aggregated_nuts_json)

# Geojson File der Landkreise (muss die Felder 'Gen' und 'Ags' beinhalten)
de_path = "necessary_files/landkreise_simplify0.geojson"
de_geo_json = geopd.read_file(de_path)

# Geojson File der NUTS Regionen, stand der Verkehrsprognose ist 2010
nuts_path = "necessary_files/NUTS_RG_01M_2010_4326.geojson"
nuts_geo_json = geopd.read_file(nuts_path)

# Koordinaten der Haltestellen
haltestellen_data = open("necessary_files/bfkoord.txt", "r", encoding="iso-8859-1")

# Zuordnung Kreisname auf KKZ
prognose_map_data_ausland_reader = csv.DictReader(open("necessary_files/Verkehrszellen_BVWP15_Ausland.csv", "r"),
                                                  delimiter=",")
prognose_map_data_ausland = []

for row in prognose_map_data_ausland_reader:
    prognose_map_data_ausland.append(row)

levl_codes = {
    "0": ["N", "FIN", "EE", "LV", "LT", "RU2", "RU1", "BY", "UA", "MD", "RO", "BG", "TR"
        , "GR", "MK", "AL", "XK", "ME", "SRB", "BIH", "HR", "SL", "ES", "PT", "IRL"]
}

tags = ["Fz1", "Fz2", "Home"]

map_esy = True
'''

Findet einen gegebenen Punkt in Deutschland oder den umliegenden EU Nationen und gibt
die zugehörige Kennzahl der Verkehrsprognose wieder, sowie einen shapely.geometry.Point und den Namen der Region.

lon: Längengrad des zu findenden Punkts
lat: Breitengrad des zu findenden Punkts
'''
def handle_region(lon, lat):
    # If not found anything use broader coords
    for i in range(8, 0, -1):
        lon = truncate(lon, i)
        lat = truncate(lat, i)

        coords = shapely.geometry.Point(lat, lon)
        # Handle Germany
        for i, kreis in enumerate(de_geo_json['geometry']):
            if kreis.contains(coords):
                print(coords, de_geo_json['GEN'][i], de_geo_json['AGS'][i])
                return coords, de_geo_json['GEN'][i], de_geo_json['AGS'][i]

        # Handle Nuts
        for i, nuts in enumerate(nuts_geo_json.get('geometry')):
            if nuts.contains(coords):

                name = nuts_geo_json['NUTS_NAME'][i]
                id = nuts_geo_json['NUTS_ID'][i]
                code = nuts_geo_json["LEVL_CODE"][i]

                if not (id in levl_codes["0"]) and code == 0:
                    continue

                for prognose in prognose_map_data_ausland:
                    if name in prognose['Bezeichnung_ME1']:
                        return coords, name, int(prognose['Nr_ME1'])

                for aggregated in aggregated_nuts_data:
                    if id in aggregated_nuts_data[aggregated]['regions']:
                        return coords, name, aggregated

        # print("Going Broader")


def map_bahn():
    csv_file = open('mappings/file_mapping_db.csv', 'w')
    csv_writer = csv.writer(csv_file)
    header = ['lon', 'lat', 'region', 'vp_ip']
    csv_writer.writerow(header)

    for line in haltestellen_data:

        line_split = line.split(' ')
        # 0 -> AreaCode     # 1 -> Longitude    # 2 -> Latitude
        line_split = [line_split[0], line_split[2], line_split[1]]

        # Bus und Bahn Verkehr
        if line_split[0].startswith('0') or line_split[0].startswith('80'):
            point, region, vp_ip = handle_region(float(line_split[1]), float(line_split[2]))

            csv_writer.writerow([float(line_split[1]), float(line_split[2]), region, vp_ip])


def map_real():

    for tag in tags:

        csv_file_writer = open('file_mapping_real_' + tag + '.csv', 'w')
        csv_writer = csv.writer(csv_file_writer)
        header = ['lon', 'lat', 'region', 'vp_ip']
        csv_writer.writerow(header)
        csv_file = open('coord_files/coords_' + tag + '.csv', 'r')
        realistic_data = csv.DictReader(csv_file.readlines())

        for row in realistic_data:
            lon = float(row['Lon'])
            lat = float(row['Lat'])
            point, region, vp_ip = handle_region(lon, lat)
            csv_writer.writerow([lon, lat, region, vp_ip])


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return float('.'.join([i, (d + '0' * n)[:n]]))


map_real()
