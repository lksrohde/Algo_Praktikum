# Erste Schritte

- Zuordnung der Verkehrszellen aus der Verflechtungsprognose zu Stationen aus dem Fahrplan
  - Amtliche Kreisschlüssel → Polygone
  - Für jede Station des Fahrplans ermitteln, in welchem Kreis sie liegt
- Aufteilung des Verkehrsaufkommens auf Stationen in den Kreisen
  - Für den Anfang: Fern- und Regionalverkehr zwischen Kreisen
- Generierung von sinnvollen Abfahrts- oder Ankunftszeiten je nach Reisezweck
- Ausgabe: Routing-Anfragen für MOTIS im JSON-Format
  - Vorwärtssuche: Startstation, Zielstation, gewünschte Abfahrtszeit
  - Rückwärtssuche: Startstation, Zielstation, gewünschte Ankunftszeit