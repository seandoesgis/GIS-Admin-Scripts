#Searches AGO webmaps for endpoints
#Author - Sean L

from arcgis.gis import GIS
from IPython.display import display
import pandas as pd
import json
import csv

portal = r"https://dvrpcgis.maps.arcgis.com"
user = ''
password = ''
gis = GIS(portal, user, password)
f=r'd:\temp\.csv'

webmaps=gis.content.search (query="", item_type="Web Map", max_items=5000)
with open(f, 'w', newline='') as fout:
    writer = csv.writer(fout)
    for webmap in webmaps:
        webmapJSON = webmap.get_data()
        for layer in webmapJSON['operationalLayers']:
            url=layer.get('url')
            if url:
                if "CMP_SubcorridorsEmergingCorridors" in url:
                    list=[[webmap.title,webmap.id,webmap.owner,url]]
                    writer.writerows(list)
            else:
                pass