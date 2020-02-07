##Catalogs directories that include shapefiles and feature classes within file geodatabases, ouputs directory name and file name to CSV
##Written by Sean L for DVRPC, 2016

import os,csv,arcpy

##name output csv
f=open(r"d:\temp\GIS.csv",'wb')
w=csv.writer(f)
##table header
w.writerow(["Directory","GIS file"])
##directory you want to inventory
rootdir =r'P:'
##directory walk
for dirName, subdirList, fileList in os.walk(rootdir):
##    geodatabase feature class search
    if dirName.endswith(".gdb"):
        arcpy.env.workspace=dirName
        features=arcpy.ListFeatureClasses()
        for feature in features:
            w.writerow([dirName,feature])
##    shapefile search
    for fname in fileList:
        if fname.endswith(".shp"):
            w.writerow([dirName,fname])
##sde geodatabase feature class search
    # for fname in fileList:
    #     path=dirName+"\\"+fname
    #     arcpy.env.workspace=path
    #     features=arcpy.ListFeatureClasses()
    #     for fc in features:
    #         w.writerow([dirName,fc])

f.close()
