---
geometry: margin=2cm
title: Algorithmen Praktikum 
author: Lukas Rohde
date: 14.4.2021
---

Die Abgabe besteht aus 3 verschiedenen Skripts, welche aufeinander aufbauen. Die Skripte erstellen jeweils Files, welche
in den dazugehörigen Ordnern unter "src/" zu finden sind.

## get_osm_tags_as_coords
Dieses Skript findet die Koordinaten von definierbaren OSM Tags in einem definierbaren OSM Datensatz. 

Zur Anpassung vor der Verwendung können im Skript die Attribute angepasst werden. Es sind zwei verschiedene Bibliotheken verwendet worden, pyrosm verwendet eine große Menge an RAM bietet aber die Möglichkeit
automatisch .pbf Files selbst zu beziehen. Esy-osmfilter verwendet weniger Ram und bietet mehr Filteroptionen erzeugt allerdings extra files.   
Um zwischen den zwei Filterarten switchen zu können muss nur der bool "build_with_esy" gesetzt werden.   

**osm_tags** kann im Format: "TAG_NAME": {GROUP1: [ELEMENT1, ELEMENT2], GROUP2: [ELEMENT1, ELEMENT2]} angepasst werden, um treffende Nodes aus den gegebenen pbf Files zu filtern und die entsprechenden Koordinaten auszugeben.   
**tags** ist eine Liste, welche die Namen der Tags beinhalten muss, welche noch geprüft werden sollen. Da die Tags jeweils direkt geschrieben werden, nachdem er fertig überprüft wurde, kann diese List hilfreich sein, um die Berechnung später fortzusetzen.
   
#### Pyrosm   

**regions** muss auf einen von pyrosm zur Verfügung gestellten Datensatz konfiguriert werden. Dieser Datensatz wird dann in src/osm-pbf gesucht und falls nicht gefunden von Geofabrik automatisch bezogen.   
   
#### Esy-Osmfilter
Der Filter wird automtisch die .pbf Files im Ordner src/osm-pbf parsen.

Sind alle Einstellungen so vorgenommen, wie gewünscht werden in den Ordner src/coords_files die gefundenen Koordinaten zu jedem Tag in eine eigene Datei geschrieben.
   
## coordinate_matcher
Es ist möglich ein Bahn spezifisches oder ein mapping File basierend auf den coordinate Files aus dem vorherigen Skript zu generieren.
Sowohl das Bahn Mapping, als auch das reale Mapping sind notwendig um im nächsten Schritt vollständige Reiseketten zu generieren!
Es müssen lediglich die Tags angegeben werden, welche zu den Koordinaten Files korrespondieren.
   
## generate_traffic
Das letzte Skript erzeugt nun eine csv, welche jeweils zu Koordinaten beinhaltet, eine Uhrzeit, sowie einen Tag, welcher angibt ob es sich um eine reverse
Traffic suche handelt oder eine forwards Suche.   
Zu konfigurieren sind nur die Wahrscheinlichkeit, mit der entschieden wird, ob die Quelle zufällig gewählt wird, oder aus dem "Home" Tag
genommen wird, sowie der Tag in Unixzeit. Außerdem lassen sich wahlweise auch die Verkehrszeiten der einzelnen Tags neu angeben.