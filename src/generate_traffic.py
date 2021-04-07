import csv
import os
import random
import time

dataPath = os.path.dirname(__file__) + "/data"
trafficPath = dataPath + "/sensibleData/verkehrsverflechtungsprognose/PVMatrix_BVWP15_P2030/PVMatrix_BVWP15_P2030.csv"
matchedFahrplan = dataPath + "/haltestellen_mapped.json"

classes = {
        "Fz1" : [{"start" : 360 , "inter" : 540 - 360}, {"start" : 960 , "inter" : 1140 - 960}] ,   # 6 - 9 -- 16 - 19  (360 - 540 -- 960 - 1140)
        "Fz2" : [{"start" : 360 , "inter" : 540 - 360}, {"start" : 960 , "inter" : 1140 - 960}] ,   # 6 - 9 -- 16 - 19  (360 - 540 -- 960 - 1140)
        "Fz3" : [{"start" : 540 , "inter" : 960 - 540}],                                            # 9 -- 16           (540 - 960)
        "Fz4" : [{"start" : 360 , "inter" : 540 - 360}, {"start" : 960 , "inter" : 1140 - 960}],    # 6 - 9 -- 16 - 19  (360 - 540 -- 960 - 1140)
        "Fz5" : [{"start" : 180 , "inter" : 540 - 180}, {"start" : 900 , "inter" : 1200 - 900}],    # 3 - 9 -- 15 - 20  (180 - 540 -- 900 - 1200)
        "Fz6" : [{"start" : 0 , "inter" : 1440}]                                                    # 0-24          (0 - 1440)
    }
mapping_dict = {}

def generate_dict():
    csv_mapping_file = open("file_mapping.csv", "r")
    csv_mapping = csv.reader(csv_mapping_file)
    mapping = []
    for line in csv_mapping:
        mapping.append(line)
        mapping_dict[line[3]] = []

    for line in mapping:
        mapping_dict[line[3]].append(line[0])

    print("Finished Dict")

def iterate_threw_traffic():
    csv_traffic = open(trafficPath, encoding='utf-8')
    traffic = csv.DictReader(csv_traffic, delimiter=';')

    verkehrsmittel = ["Bahn", "OESPV"]
    verkehrsarten = ["Fz1", "Fz2", "Fz3", "Fz4", "Fz5", "Fz6"]

    csv_file = open('reisekette_v03.csv', 'w')
    csv_writer = csv.writer(csv_file)
    header = ['quelle', 'ziel', 'zeit', 'reverse']
    csv_writer.writerow(header)

    for mappings in traffic:
        for mittel in verkehrsmittel:
            for art in verkehrsarten:
                mittel_art = mittel + "_" + art

                traffic_akt = round(int(mappings[mittel_art]) / 365)

                for i in range(traffic_akt):
                    time = get_random_time(art)
                    re = random.randint(0, 1)

                    if re == 1:
                        time = time + 3600

                    quelle = get_random_haltestelle(mappings["# Quelle"])
                    ziel = get_random_haltestelle(mappings["Ziel"])

                    if quelle == -1 or ziel == -1:
                        continue

                    csv_writer.writerow([quelle, ziel, time, re])

def get_random_haltestelle(kkz):

    try:
        relevant_class = mapping_dict[kkz]
        if len(relevant_class) == 1:
            return relevant_class[0]
        else:
            return relevant_class[random.randrange(len(relevant_class) - 1)]
    except:
        return -1

def get_realistic_haltestelle(kkz):
    return -1

def get_random_time(fzg_klasse):

    relevant_class = classes[fzg_klasse]
    if len(relevant_class) == 1:
        i = 0
    else:
        i = random.randrange(len(relevant_class) - 1)

    time_of_day = (relevant_class[i]["start"] * 60 + random.randrange(relevant_class[i]["inter"]) * 60)
    return 1616626800 + time_of_day

generate_dict()
iterate_threw_traffic()

