import csv
import os

import pyrosm
from esy.osmfilter import run_filter
from esy.osmfilter import Node, Way, Relation

osm_tags = {
    "Fz1": {"landuse": ["commercial"], "building": ["commercial", "industrial", "office"]},
    "Fz2": {"amenity": ["college", "school", "university"]},
    "Home": {"building": ["apartments", "bungalow", "cabin", "detached", "dormitory", "house", "residential"],
             "landuse": ["residential"]}
}

# Versucht automatisch pbf files in "osm-pbf" zu dem gewählten Datensatz zu finden
# Bsp Datensätze sind:
# "pyrosm.data.sources.subregions.germany" -> Alle Subregionen von Deutschland
# "pyrosm.data.Europe.regions" -> Alle Länder in Europa
regions = pyrosm.data.sources.europe.regions

tags = ["Fz2", "Home"]

build_with_esy = True


def build_files(tag):
    if __name__ == '__main__':

        pbf_input = "osm-pbf/"

        coords_list = []

        for region in regions:
            print("Next Region: " + region)

            file = pyrosm.get_data(region, directory=pbf_input)

            print("Got File!")

            osm = pyrosm.OSM(file)

            print("Loaded File!")

            data = osm.get_data_by_custom_criteria(custom_filter=osm_tags[tag], filter_type="keep", keep_nodes=True,
                                                   keep_ways=False,
                                                   keep_relations=False)

            centroids = data.centroid

            for i, coords in enumerate(centroids.x):
                coords_list.append([centroids.x[i], centroids.y[i]])

            print("Filtered threw File!")
            print(" ")

        csv_file = open('coord_files/test_coords_' + tag + '.csv', 'w')
        csv_writer = csv.writer(csv_file)

        csv_writer.writerows(coords_list)


def build_files_esy(tag):
    pbf_input = "osm-pbf/"
    json_out = "esy_out/" + tag + "/"

    prefilter = {Node: osm_tags[tag], Way: osm_tags[tag], Relation: osm_tags[tag]}

    whitefilter = []
    blackfilter = []

    csv_out = open("coord_files/coords_" + tag + ".csv", "w")
    csv_writer = csv.writer(csv_out)
    csv_writer.writerow(["Lat", "Lon"])

    for pbf in os.listdir(pbf_input):
        print(pbf)
        try:
            json = json_out + pbf + ".json"

            [data, _] = run_filter(tag, pbf_input + pbf, json, prefilter, whitefilter, blackfilter, True, False, False,
                                   True)

            lon_lat = []
            for node in data['Node']:
                lonlat = data['Node'][node]['lonlat']
                lon_lat.append([lonlat[0], lonlat[1]])
            csv_writer.writerows(lon_lat)

        except:
            print(pbf)
            continue


if __name__ == '__main__':
    for tag in tags:

        if build_with_esy:
            build_files_esy(tag)
        else:
            build_files(tag)

        print("Finished Parsing all Regions.")

    print("Finished all Tags")
