"""
                    Put trail_damage.dat into more usable form

Randy Direen
10/1/2014

Data is currently all in strings and human readable form. This script attempts
to put numbers such as elevation into numerical format.

"""
import re

def format_data(tddata):
    trails = {}
    for trail in tddata:
        id = int(trail["ID"])
        trails[id] = {}

        trails[id]["lat_lng"] = [float(trail["map"]["lat"]),
                                 float(trail["map"]["lng"])]
        trails[id]["name"] = trail["map"]["trail"]
        trails[id]["county"] = trail["map"]["county"]

        if "Elevation" in trail["info"]:
            pat = re.compile(r'\s*([0-9,]+)\s*to\s*([0-9,]+)')
            fnd = pat.match(trail["info"]["Elevation"])
            if fnd:
                gs = [int(val.replace(",",""))  for val in fnd.groups()]
                trails[id]["Elevation"] = gs
            else:
                trails[id]["Elevation"] = trail["info"]["Elevation"]
        else:
            trails[id]["Elevation"] = None

        if "Location" in trail["info"]:      
            trails[id]["Location"] = trail["info"]["Location"]
        else:
            trails[id]["Location"] = None

        if "TrailType" in trail["info"]:      
            trails[id]["TrailType"] = trail["info"]["TrailType"]
        else:
            trails[id]["TrailType"] = None

        if "TrailLength" in trail["info"]: 
            pat = re.compile(r'\s*([0-9.]+)\s*mile')
            fnd = pat.match(trail["info"]["TrailLength"])
            if fnd:
                trails[id]["TrailLength"] = float(fnd.groups()[0])
            else:
                trails[id]["TrailLength"] = trail["info"]["TrailLength"]     
        else:
            trails[id]["TrailLength"] = None

        trails[id]["legend"] = trail["info"]["legend"]

        if "NearbyTrails" in trail["info"]:      
            trails[id]["NearbyTrails"] = trail["info"]["NearbyTrails"]
        else:
            trails[id]["NearbyTrails"] = None

        if "NearbyTowns" in trail["info"]:      
            trails[id]["NearbyTowns"] = trail["info"]["NearbyTowns"]
        else:
            trails[id]["NearbyTowns"] = None

        trails[id]["updated"] = trail["updated"]
        trails[id]["description"] = trail["description"]
        trails[id]["directions"] = trail["directions"]

    return trails

def slim_data(trails):
    strails = []
    for item in trails:
        strail = {}
        strail["id"] = item
        strail["name"]  = trails[item]["name"]
        strail["lat_lng"] = trails[item]["lat_lng"]
        strail["legend"] = {}
        strail["legend"]["low_rating"] = trails[item]["legend"]["Low-End Rating:"]
        strail["legend"]["high_rating"] = trails[item]["legend"]["High-End Rating:"]
        strail["legend"]["scenery"] = trails[item]["legend"]["Scenery:"]
        strail["legend"]["elevation"] = trails[item]["legend"]["Elevation:"]
        strail["legend"]["rock_crawling"] = trails[item]["legend"]["Rock Crawling:"]
        strail["legend"]["climbs_descents"] = trails[item]["legend"]["Climbs & Descents:"]
        strail["legend"]["water_crossing"] = trails[item]["legend"]["Water Crossings:"]
        strail["legend"]["cliffs_ledges"] = trails[item]["legend"]["Cliffs & Ledges:"]
        strail["legend"]["dirt_mud"] = trails[item]["legend"]["Dirt & Mud:"]
        strail["legend"]["playgrounds"] = trails[item]["legend"]["Playgrounds:"]
        strail["directions"] = trails[item]["directions"]
        strail["nearby_towns"] = trails[item]["NearbyTowns"]
        strail["nearby_trails"] = trails[item]["NearbyTrails"]
        strail["elevation"] = trails[item]["Elevation"]
        strail["trail_length"] = trails[item]["TrailLength"]
        strail["trail_type"] = trails[item]["TrailType"]
        strail["county"] = trails[item]["county"]
        strail["updated"] = trails[item]["updated"]

        strails.append(strail)

    return strails


if __name__ == "__main__":
    import pickle
    tddata = pickle.load( open(r'scrap\trail_damage.dat', "rb" ) )

    dat = format_data(tddata)
    sdat = slim_data(dat)

    for item in sdat:
        print item





    a = raw_input()