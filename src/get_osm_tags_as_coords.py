import overpy
import os
import csv
import esy.osmfilter
from esy.osmfilter import run_filter
from esy.osmfilter import Node, Way, Relation
import pyrosm
import geopandas as geopd

dataPath = os.path.dirname(__file__) + "/data"

osm_countries = ["Deutschland"]

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

osm_tags_rebuild = {
    "Fz1": {"landuse": ["commercial"], "building": ["commercial", "industrial", "office"]},
    "Fz2": {"amenity": ["college", "school", "university"]},
    "Home": {"building": ["apartments", "bungalow", "cabin", "detached", "dormitory", "house", "residential"]}
}

def build_query(tag, country):
    query = '[out:json][timeout:1200]; area[name="' + country + '"]->.searchArea; ('
    for string in osm_tags[tag]:
        query = query + "relation[" + string + "](area.searchArea); "
    query = query + "); out center;"
    print(query)
    return query

def use_overpass():
    api = overpy.Overpass()

    for country in osm_countries:
        output_file_json = open(dataPath + "/osm_pointData/osm_points_" + country + ".json", "a")
        print("Country: " + country)
        for tag in osm_tags:
            print("Tag: " + tag)
            query = build_query(tag, country)
            json_dump = api.query(query).__dict__

            output_file_json.write(json_dump.__str__())

def use_local():
    def find_already_parsed(dir):
        output = []
        for d in os.walk(dir):
            output.append(d[0])
        return output

    if __name__ == '__main__':
        tag = "Fz2"
        subregions = pyrosm.data.sources.subregions
        pbf_input = dataPath + "/osm-pbf/"
        output = dataPath + "/osm-pbf/out/"

        print(subregions.germany.available)
        already_parsed = find_already_parsed(output)

        for region in subregions.germany.available:
            print(region)

            skip = False
            for parsed in already_parsed:
                if region in parsed:
                    skip = True
            if skip: continue

            file = pyrosm.get_data(region, directory=pbf_input)

            print(region + " Downloaded!")
            output = dataPath + "/osm-pbf/out/" + region + "_" + tag

            osm = pyrosm.OSM(file)

            # Latitude, Longitude in Geometry
            data = osm.get_data_by_custom_criteria(custom_filter=osm_tags_rebuild[tag], filter_type="keep", keep_nodes=False, keep_ways=True,
                                            keep_relations=True)
            centroids = data.centroid

            # centroids.to_file(export_file)
            geopd.GeoSeries.to_file(centroids, output)


use_local()
