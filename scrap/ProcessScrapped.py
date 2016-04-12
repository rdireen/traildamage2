"""
                        Put the data in the tddata/ folder
                             into trail_damage.dat 

Randy Direen
10/1/2014


"""

import requests
import glob
import re
import json
import pickle
from td_methods import grab_trails_colorado

s = """
This script takes all of the trails saved in tddata and puts them into a 
single list trail_damage.dat. It also checks to see if there are any new
trails that haven't been scrapped yet.

Run this script after ScrapTrailDamage.py


"""
print s

rex = re.compile(r'trail_([0-9]+).p')
r = requests.get("http://traildamage.com/google_colorado_writer.php")
trails = grab_trails_colorado(r)

dmap = {}
for trail in trails:
    dmap[trail["trail_id"]] = trail


ids_fresh = [trail["trail_id"] for trail in trails]

ids = []
trail_data = []
for filename in glob.glob(r'tddata\*.p'):
    ID = rex.search(filename).groups()[0]
    ids.append(ID)

    strng = pickle.load( open(filename, "rb" ) )
    dat = json.loads(strng)

    dat["map"] = dmap[ID]
    trail_data.append(dat)

pickle.dump( trail_data, open( 'trail_damage.dat', "wb" ) )

for id in ids_fresh:
    if id not in ids:
        print "Data not up to date. Need id = %s" % id



    

a = raw_input()