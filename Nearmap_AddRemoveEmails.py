import psycopg2,pandas,json,urllib,requests

conn=psycopg2.connect("dbname=postgres user=postgres password= host=gis-db")
sql="select * from public.stafflist;"
df=pandas.read_sql_query(sql,conn)
cur=conn.cursor()

id_df_list = df['id'].tolist()
intranet_list=[]

url = "http://intranet.dvrpc.org/stafflist/MyData.aspx"
response = urllib.urlopen(url)
data = json.load(response)
dataset=data['data']

for staff in dataset:
    id=staff['ID']
    intranet_list.append(id)

remove=set(id_df_list) - set(intranet_list)
add=set(intranet_list) - set(id_df_list)


for i in dataset:
    if i['ID'] in add:
        id=i['ID']
        first=i['FIRSTNAME']
        last=i['LASTNAME']
        cur.execute("INSERT INTO public.stafflist (first,last,email,id) VALUES (%s, %s, %s,%s)", (first, last, id+'@dvrpc.org',id))
        datad ={"content" : "Please add "+id+"@dvrpc.org, to the nearmap user list"}
        requests.post(url='discord webhook', data=datad)
for o in remove:
    cur.execute("DELETE FROM public.stafflist WHERE id = '{}';".format(o))
    datad = {"content": "Please remove "+o+"@dvrpc.org, from the nearmap user list"}
    requests.post(url='discord webhook', data=datad)

conn.commit()
cur.close()
conn.close()
