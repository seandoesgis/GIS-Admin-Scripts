from arcgis.gis import GIS
import urllib.parse as urlp
import urllib.request as urlr
import json

#add login and password to gis
gis = GIS("https://arcgis.dvrpc.org/dvrpc", "", "")

gis_servers = gis.admin.servers.list()
server = gis_servers[0]
folders = server.services.folders

parameters = urlp.urlencode({'username' : '', 'password' : '','client' : 'referer','referer': 'https://arcgis.dvrpc.org/dvrpc','expiration': 15,'f' : 'json'})
binaryparameters=parameters.encode()
response = urlr.urlopen('https://arcgis.dvrpc.org/dvrpc/sharing/rest/generateToken?',binaryparameters).read()
response_obj = json.loads(response)
token=response_obj.get('token')

for folder in folders:
	services = server.services.list(folder=folder)
	for service in services:
		params = urlp.urlencode({'token':token,'f': 'json'})
		binaryparams=params.encode()
		resp = urlr.urlopen(service.url,binaryparams).read()
		dataObj = json.loads(resp)
		extension = dataObj['extensions']
		for a in extension:
			typename = a['typeName']
			enab = a['enabled']
			if typename == 'WFSServer' and enab == 'false':
				a['enabled']='true'
				editSvcURL = service.url+"/edit"
				print (editSvcURL)
				params2 = urlp.urlencode({'token': token, 'f': 'json', 'service': dataObj})
				binaryparams2=params2.encode()
				req = urlr.Request(editSvcURL,binaryparams2)
				# resp2 = urlr.urlopen(req)
				# print (resp2)





				











