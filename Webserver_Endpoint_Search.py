#Search webserver for specific api endpoints
#Author - Will T

import csv, os, re
i = r"s:\\"
o = r"d:\temp\ago_services_apps.csv"
x = ['.htm','html','.js','.json']
e = r'[^"\']*services1\.arcgis\.com[^"\']*'
def a(f):
    with open(f) as io:r = [re.findall(e,l) for l in list(io) if re.search(e,l)]
    return r
with open(o, "wb") as io:csv.writer(io).writerows([(p,u) for (p, uss) in map(lambda (f,t,p):(p,a(p)),filter(lambda (f,t,p):t in x,[os.path.splitext(f.lower())+(os.path.join(r,f),) for r,d,fs in os.walk(i) for f in fs])) for us in uss for u in us if us])