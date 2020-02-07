#Count licenses in license manager log file, run on gis-portal

import sys
import re

def main():
    lines = []
    try:
        with open (r'C:\Program Files (x86)\ArcGIS\LicenseManager\bin\lmgrd9.log', "r") as inp:
            lines=inp.readlines()
    except IOError as e:
        print e
        print "Usage: %s logfile" % sys.argv[0]
        return 1
    hosts = set()
    features = set()

    outs = dict()
    for l in lines:
        m = re.search(r'\((\w+)\)\s+OUT:\s+"(.+)"\s+([^\s]+@[^\s]+)', l)
        if m:
            vendor  = m.group(1)
            feature = m.group(2)
            user    = m.group(3).split("@")[0]
            host    = m.group(3).split("@")[1]
            # Now try to get how many licenses has been acquired
            m = re.search(r'\((\d+)\s+licenses\)', l)
            if m: n_lic = int(m.group(1))
            else: n_lic = 1

            features.add(feature)
            if not (user in outs):
                outs[user] = dict()
            if not (feature in outs[user]):
                outs[user][feature] = n_lic
            else:
                outs[user][feature] = outs[user][feature] + n_lic

    # Users and features they've checked out, in total
    for u in outs.keys():
        print "User %s total checkouts:" % u
        for f in outs[u].keys():
            print "{:<32} {:>5}".format(f, outs[u][f])
        print ""

if __name__ == "__main__":
    main()
