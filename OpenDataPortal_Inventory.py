#catalog all data in DVRPC Open Data Portal
#author - Sean L

import urllib,json,csv

url = "http://dvrpc.dvrpcgis.opendata.arcgis.com/data.json"
##name output csv
f=open(r"d:\temp\ODP.csv",'wb')
w=csv.writer(f)
##table header
w.writerow(["Name","RestAPI", "GeoJSON","CSV","Shapefile"])
response = urllib.urlopen(url)
data = json.load(response)
dataset=data['dataset']

for feature in dataset:
    featureTitle=feature['title']
    for details in [feature]:
        distribution=details['distribution']
        restLink=""
        geojsonLink=""
        csvLink=""
        zipLink=""
        for i in distribution:
            test=i.get('format')
            if test == 'Esri REST':
                restLink=i['accessURL']
            if test == 'GeoJSON':
                geojsonLink=i['downloadURL']
            if test == 'CSV':
                csvLink=i['downloadURL']
            if test == 'ZIP':
                zipLink=i['downloadURL']
        w.writerow([featureTitle,restLink,geojsonLink,csvLink,zipLink])
f.close()


