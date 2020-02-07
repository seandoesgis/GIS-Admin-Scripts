##Script to add/delete new Viewer accounts for DVRPC GIS Portal based on intranet staff list
##Author: Sean L

import urllib,json
from arcgis.gis import GIS

gis = GIS("https://gis-portal.dvrpc.org/arcgis/home/")
users = gis.users.search(outside_org=False, max_users=500,role='iAAAAAAAAAAAAAAA')
portaluserlist=[]
stafflist=[]

for user in users:
    userid=user.username.split('@')[0]
    portaluserlist.append(userid)

url = "http://intranet.dvrpc.org/stafflist/MyData.aspx"
response = urllib.request.urlopen(url)
data = json.load(response)
dataset=data['data']

for person in dataset:
    dept=person['DEPARTMENT']
    if dept != 'GIS':
        id=person['ID']
        stafflist.append(id)

remove=set(portaluserlist) - set(stafflist)
add=set(stafflist) - set(portaluserlist)

##print(remove)
##print(add)

for staff in remove:
    staffobj=gis.users.get(staff+'@DVRPC_PRIMARY')
    staffobj.delete()

for i in dataset:
    if i['ID'] in add:
        id=i['ID']
        first=i['FIRSTNAME']
        last=i['LASTNAME']
        gis.users.create(username=id+'@DVRPC_PRIMARY',idp_username=id+'@DVRPC_PRIMARY', password= '', firstname =first, lastname = last, email = id+'@dvrpc.org' , role='iAAAAAAAAAAAAAAA', user_type='Viewer',provider='enterprise')








