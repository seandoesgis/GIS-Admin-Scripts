# - DCAT writter for DVRPC GIS Portal

import json
import urllib.parse as urlp
import urllib.request as urlr
import datetime as dt
from collections import OrderedDict
import os

parameters = urlp.urlencode({'username' : '', 'password' : '','client' : 'referer','referer': 'https://arcgis.dvrpc.org/dvrpc','expiration': 3,'f' : 'json'})
binaryparameters=parameters.encode()
response = urlr.urlopen('https://arcgis.dvrpc.org/dvrpc/sharing/rest/generateToken?',binaryparameters).read()
response_obj = json.loads(response)
token=response_obj.get('token')

url=r'https://arcgis.dvrpc.org/dvrpc/sharing/rest/search?f=json&q=(group%3Aa7fd0fac370846c784cc7a4e50c19ae7%20OR%20group%3Ae22b17eb25964eeabc5108f5e16ae785%20OR%20group%3A19c2762c1e9c46ee9bff55a4dc212057%20OR%20group%3A2c6beaa1b3d247978b5784d9033fa631%20OR%20group%3Ad8d9fe9c058b490ba7c5aeda07ba261e%20OR%20group%3Acaaeea60fce64aa88f7be57c125f8572%20OR%20group%3Acad82d384885451ba82673b92b8b42eb%20OR%20group%3A2627d44ad5744c91a456cde0843f7dcc%20OR%20group%3Afa0df7c75e0a4418881ba14e04475da7%20OR%20group%3Ac8ce45d92f7a42df86daa450f90835ed%20OR%20group%3Ab2da3d4a7fb04708ba994d4909b4b869%20OR%20group%3Ab195734907e8476e8f45ac48fdfc2bc0)&start=1&num=200&token='+token
response = urlr.urlopen(url)
portaldata = json.load(response)
results=portaldata['results']

intro='{"@context":"https://project-open-data.cio.gov/v1.1/schema/catalog.jsonld","@type":"dcat:Catalog","conformsTo":"https://project-open-data.cio.gov/v1.1/schema","describedBy":"https://project-open-data.cio.gov/v1.1/schema/catalog.json"}'
dcat = json.loads(intro,object_pairs_hook=OrderedDict)
dcat['dataset']=[]

for item in results:
	id=item['id']
	title=item['title']
	description=item['description']
	secondsmod=item['modified']
	modified=dt.datetime.utcfromtimestamp(secondsmod/1000).isoformat()
	secondscr=item['created']
	issued=dt.datetime.utcfromtimestamp(secondscr/1000).isoformat()
	keyword=item['tags']
	access=item['access']
	serviceurl=item['url']

	urlp.urlparse(serviceurl)
	path=urlp.urlparse(serviceurl).path[1:]
	parts = path.split('/')
	['/' + '/'.join(parts[:index+1]) for index in range(len(parts))]
	wfsbaseurl='https://arcgis.dvrpc.org/portal/services/'+parts[3]+'/'+parts[4]+'/MapServer/WFSServer'
	wfscapurl='https://arcgis.dvrpc.org/portal/services/'+parts[3]+'/'+parts[4]+'/MapServer/WFSServer?request=GetCapabilities&service=WFS'
	geojsonurl=item['url']+'/0/query?where=1=1&outfields=*&outsr=4326&f=geojson'
	#thumbnailurl=r'https://arcgis.dvrpc.org/dvrpc/sharing/rest/content/items/'+id+'/info/thumbnail/thumbnail.JPEG'
	metadataurl=serviceurl+'/0/metadata'
	htmlurl='https://arcgis.dvrpc.org/dvrpc/home/webmap/viewer.html?useExisting=0&layers='+id+'&layerId=0'
	csvurl=wfsbaseurl+'?request=GetFeature&service=WFS&typename='+parts[4]+'&outputformat=csv%2Bzip&format_options=filename:'+parts[4]+'.zip'
	netpath= os.path.join('V:', parts[3],parts[3]+'.sde',parts[4])
	networkpath= os.path.normpath(netpath)

	#spatial=item['extent']


	data={"@type":"dcat:Dataset","identifier":id,"title":title,"description":description,"keyword":keyword,"issued":issued,"modified":modified,"publisher":"DVRPC GIS","contactPoint":{"@type":"vcard:Contact","fn":"Delaware Valley Regional Planning Commission","hasEmail": "mailto:slawrence@dvrpc.org"},"accessLevel":access,"distribution":[{"@type":"dcat:Distribution","title":"Esri Rest API","format":"Esri REST","mediaType":"application/json","accessURL":serviceurl},{"@type":"dcat:Distribution","title":"GeoJSON","format":"GeoJSON","mediaType":"application/geo+json","accessURL":geojsonurl},{"@type":"dcat:Distribution","mediaType":"text/html","accessURL":htmlurl},{"@type":"dcat:Distribution","mediaType":"application/xml","accessURL":metadataurl},{"@type":"dcat:Distribution","title":"CSV","format":"CSV","mediaType":"text/csv","downloadURL":csvurl},{"@type":"dcat:Distribution","mediaType":"application/vnd.ogc.wfs_xml","format": "OGC WFS","title": "OGC WFS","accessURL":wfscapurl},{"@type":"dcat:Distribution","title":"Network Location","format":"ESRI Feature Class","downloadURL":networkpath}]}


	dcat['dataset'].append(data)

with open('/Users/seanlawrence/Desktop/data.json', 'w') as outfile:
    json.dump(dcat, outfile)
