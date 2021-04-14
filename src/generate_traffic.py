import csv
import os
import random

dataPath = os.path.dirname(__file__) + "/data"
trafficPath = dataPath + "/PVMatrix_BVWP15_P2030.csv"
perTagFiles = dataPath + "/osm-pbf/"

day = 1616626800
prob_quelle_random = 0.15
out_name = 'reisekette_v1.1'

# Outputfile
csv_file = open('reiseketten/' + out_name + '.csv', 'w')
csv_writer = csv.writer(csv_file)

# Init Outputfile und Format
header = ['q_lat', 'q_lon', 'z_lat', 'z_lon', 'zeit', 'reverse']
csv_writer.writerow(header)

classes = {
    "Fz1": [{"start": 420, "inter": 540 - 420, "re": 1}, {"start": 960, "inter": 1140 - 960, "re": 0}],
    "Fz2": [{"start": 360, "inter": 540 - 360, "re": 1}, {"start": 960, "inter": 1140 - 960, "re": 0}],
    "Fz3": [{"start": 540, "inter": 960 - 540, "re": 0}],
    "Fz4": [{"start": 360, "inter": 540 - 360, "re": 1}, {"start": 960, "inter": 1140 - 960, "re": 0}],
    "Fz5": [{"start": 180, "inter": 540 - 180, "re": 1}, {"start": 900, "inter": 1200 - 900, "re": 0}],
    "Fz6": [{"start": 0, "inter": 1440, "re": 0}]
}

mapping_dict = {}
mapping_dict_home = {}
mapping_dict_db = {}


def generate_mapping_dict_db():
    csv_mapping_file = open("mappings/file_mapping_db.csv", "r")
    csv_mapping = csv.reader(csv_mapping_file)
    mapping = []

    for line in csv_mapping:
        mapping.append(line)
        mapping_dict_db[line[4]] = []

    for line in mapping:
        mapping_dict_db[line[4]].append((line[1], line[2]))

    print("Finished Bahn mapping Dict")


def generate_mapping_dict_real(fz):
    csv_mapping_file = open("mappings/file_mapping_real_" + fz + ".csv", "r")
    csv_mapping = csv.reader(csv_mapping_file)
    mapping = []
    local_mapping_dict = {}

    for line in csv_mapping:
        mapping.append(line)
        local_mapping_dict[line[3]] = []

    for line in mapping:
        local_mapping_dict[line[3]].append((line[1], line[0]))

    print("Finished real mapping Dict")
    return local_mapping_dict


def iterate_threw_traffic(tag):
    # Open Verkehrsprognose
    csv_traffic = open(trafficPath, encoding='utf-8')
    traffic = csv.DictReader(csv_traffic, delimiter=';')

    # Relevante Verkehrsmittel und Arten
    verkehrsmittel = ["Bahn", "OESPV"]




    for mappings in traffic:
        for mittel in verkehrsmittel:

            mittel_art = mittel + "_" + tag

            # Relevanter traffic pro Tag
            traffic_akt = round(int(mappings[mittel_art]) / 365)

            # Generate Traffic pro Bewegung am Tag
            for i in range(traffic_akt):

                # Zufällige Zeit und dazugehörger Reversetag
                # re e [0,1]
                re, time = get_time(tag)

                quelle, ziel = get_realistic_haltestelle(mappings["# Quelle"], mappings["Ziel"], re)

                # Skip, falls Problem auftritt mit Haltestelle
                if quelle == -1 or ziel == -1:
                    continue

                csv_writer.writerow([quelle[0], quelle[1], ziel[0], ziel[1], time, re])


def get_random_haltestelle(kkz):
    try:
        relevant_class = mapping_dict_db[kkz]
        if len(relevant_class) == 1:
            return relevant_class[0]
        else:
            return relevant_class[random.randrange(len(relevant_class) - 1)]
    except:
        return -1


def get_realistic_haltestelle(quelle, ziel, re):
    try:
        # Quelle: Home oder Random -> Ziel immer Tag
        if re == 0:
            if random.randrange(0, 100, step=1) > prob_quelle_random * 100:
                try:
                    relevant_class_quelle = mapping_dict_home[quelle]
                    quelle = relevant_class_quelle[random.randrange(len(relevant_class_quelle) - 1)]
                except:
                    quelle = get_random_haltestelle(quelle)
            else:
                quelle = get_random_haltestelle(quelle)
            try:
                relevant_class_ziel = mapping_dict[ziel]
                ziel = relevant_class_ziel[random.randrange(len(relevant_class_ziel) - 1)]
            except:
                ziel = get_random_haltestelle(ziel)

            return quelle, ziel

        # Quelle: Tag oder Random -> Ziel immer Home
        else:
            if random.randrange(0, 100, step=1) > prob_quelle_random * 100:
                try:
                    relevant_class_quelle = mapping_dict[quelle]
                    quelle = relevant_class_quelle[random.randrange(len(relevant_class_quelle) - 1)]
                except:
                    quelle = get_random_haltestelle(quelle)

            else:
                quelle = get_random_haltestelle(quelle)

            try:
                relevant_class_ziel = mapping_dict_home[ziel]
                ziel = relevant_class_ziel[random.randrange(len(relevant_class_ziel) - 1)]
            except:
                ziel = get_random_haltestelle(ziel)

            return quelle, ziel
    except:
        return -1, -1


def get_time(fzg_klasse):
    relevant_class = classes[fzg_klasse]

    i = random.randrange(0, len(relevant_class))

    time_of_day = (relevant_class[i]["start"] * 60 + random.randrange(0, relevant_class[i]["inter"]) * 60)
    return relevant_class[i]["re"], day + time_of_day


# Dict für Homes in erkannten Regionen
mapping_dict_home = generate_mapping_dict_real("Home")
generate_mapping_dict_db()



tags = ["Fz2", "Fz3", "Fz4", "Fz5", "Fz6"]

for tag in tags:
    try:
        mapping_dict = generate_mapping_dict_real(tag)
    except:
        print("No Tag found, using random data based on DB")
        mapping_dict = mapping_dict_db
    iterate_threw_traffic(tag)
