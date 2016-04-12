"""
                            Scrap traildamage.com

Randy Direen
10/1/2014

Scraps all of the trails off of traildamage.com and puts the results in the 
tddata/ folder. This script takes about a half an hour to run right now 
because I wait 5 seconds between each call to traildamage.com.


"""

from td_methods import *
import time
import pickle
import json

print """********************************************************************************

    traildamage.com scrapper

    Randy Direen
    10/1/2014

********************************************************************************"""

r = requests.get("http://traildamage.com/google_colorado_writer.php")

trails = grab_trails_colorado(r)

L = len(trails)

for n,trail in enumerate(trails):
    time.sleep(5)
    print "--------------------------------------------------------------------------------"
    print "Catching %d of %d trails..." % (n,L)
    print " "
    print "       Trail ID: " + trail["trail_id"]
    print "     Trail Name: " + trail["trail"]
    url = "http://www.traildamage.com/trails/index.php?id=%s" %  trail["trail_id"]
    print "            URL: " + url
  
    try:
        r = requests.get(url)
        dat = grab_traildamage_page_info(r)
        dat["ID"] = int(trail["trail_id"]) 
        filename =  r'tddata\trail_%s.p' %  trail["trail_id"]
        print "         file: " 

        stng = json.dumps(dat)
        pickle.dump( stng, open( filename, "wb" ) )
        print "     SUCCESS"
    except Exception as e:
        print "FAIL"
        print str(e)




    


a = raw_input()