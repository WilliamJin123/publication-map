import csv


def reformatMapData(path="mapData.txt"):
    """
    Reformat the map data file to include a batch header.
    """
    file = open(path, "r", encoding="utf-8")
    lines = file.read().replace('\n', '').replace('"','').replace('json','').replace('{','').replace('}','').split("```")
    file.close()
    countryDict = {}
    for line in lines:
        if line.startswith("Batch"):
            continue
        countries = line.split(",")
        for data in countries:
            if data.strip():
                country, count = data.split(":")
                country = country.strip().capitalize()
                count = int(count.strip())
                if country in countryDict:
                    countryDict[country] += count
                else:
                    countryDict[country] = count
                    
    with open("files/mapDataReformatted.csv", "w", encoding="utf-8") as output:
        csv_writer = csv.writer(output)
        csv_writer.writerow(["Country", "Count"]) # Write header row
        for country, count in countryDict.items():
            csv_writer.writerow([country, count])
           
    
if __name__ == "__main__":
    reformatMapData()

