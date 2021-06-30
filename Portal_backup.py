import urllib.parse as urlp
import urllib.request as urlr
from os import walk
import json, shutil

parameters = urlp.urlencode({'username' : 'dvrpcportaladmin', 'password' : '','client' : 'referer','referer': 'https://arcgis.dvrpc.org/dvrpc','expiration': 15,'f' : 'json'})
binaryparameters=parameters.encode()
response = urlr.urlopen('https://arcgis.dvrpc.org/dvrpc/sharing/rest/generateToken?',binaryparameters).read()
response_obj = json.loads(response)
token=response_obj.get('token')

parameters = urlp.urlencode({'location' : 'c:\backup', 'f' :'json'})
binaryparameters=parameters.encode()
response = urlr.urlopen('https://arcgis.dvrpc.org/dvrpc/portaladmin/exportSite?token='+token, binaryparameters,).read()
response_obj = json.loads(response)

f = []
for (dirpath, dirnames, filenames) in walk('d:\\temp'):
    f.extend(filenames)
    break
shutil.rmtree(r'b:\\')
shutil.move('c:\\backup\\'+f[0], 'b:\\')

