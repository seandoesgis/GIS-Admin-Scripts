#compress/rebuild/analyze SDE Databases

import arcpy
db=''
arcpy.env.workspace = ''

arcpy.AcceptConnections(db, False)
arcpy.DisconnectUser(db, "ALL")

arcpy.Compress_management(db)

##Get a list of all the datasets the user has access to.
##First, get all the stand alone tables, feature classes and rasters owned by the current user.
dataList = arcpy.ListTables() + arcpy.ListFeatureClasses()

### Next, for feature datasets owned by the current user
### get all of the featureclasses and add them to the master list.
##for dataset in arcpy.ListDatasets():
##    dataList += arcpy.ListFeatureClasses(feature_dataset=dataset)

arcpy.RebuildIndexes_management(db, "SYSTEM", dataList, "ALL")
arcpy.AnalyzeDatasets_management(db, "SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")

arcpy.AcceptConnections(db, True)