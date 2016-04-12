import cherrypy
import json
import pickle
import os
import datetime
import copy
import gpxpy
from scrap.ReformatTDdata import *


class Root(object):
    def __init__(self,data,ibeen,iadded):
        self.data = data
        for item in data:
            if len(item["updated"]) > 100:
                item["updated"] = item["updated"][0:100]
               
        self.working_data = copy.deepcopy(self.data)
        self.ibeen = ibeen
        self.iadded = iadded
        

    @cherrypy.expose
    def markers(self):
        self.working_data = copy.deepcopy(self.data)
        for item in self.working_data:
            item["ibeen_there"] = "never_there"
            item["my_last_time"] = ""
            item["my_note"]   = "Haven't been yet"
            for el in self.ibeen:
                if item["id"] == el["id"]:
                    item["ibeen_there"] = el["type"]
                    item["my_last_time"] = el["last_time"]
                    item["my_note"]   = el["note"]
                    break

        for item in self.iadded:
            self.working_data.append(item)
                    

        return json.dumps(self.working_data)


def main():
    
    tddata = pickle.load( open(r'scrap/trail_damage.dat', "rb" ) )
    dat = format_data(tddata)
    sdat = slim_data(dat)

    with open(r'scrap/test.gpx', 'r') as f:
        gpx = gpxpy.parse(f)

    ibeen = []
    iadded = []
    #places I've been
    ibeen.append({"id":290,
                  "type": "been_there",
                  "last_time":str(datetime.datetime(2014, 9, 21, 0, 0)),
                  "note":"Went here by myself. Fun bumps. Nothing to see."})
    ibeen.append({"id":12,
                  "type": "been_there",
                  "last_time":str(datetime.datetime(2014, 8, 3, 0, 0)),
                  "note":"This is that pretty lake where I took pictures of the Barhites. There is a picture of robot somewhere."})
    ibeen.append({"id":354,
                  "type": "been_there",
                  "last_time":str(datetime.datetime(2014, 9, 28, 0, 0)),
                  "note":"This is where that cool mine above George Town is that I went to with Crystal and Liz."})
    ibeen.append({"id":59,
                  "type": "been_there",
                  "last_time":str(datetime.datetime(2014, 10, 6, 0, 0)),
                  "note":"I went here with Leyna to see Torrey's Peak. Lot's of water. Cool mine stuff for melting things. McLellan is the fun path."})
    ibeen.append({"id":60,
                  "type": "been_there",
                  "last_time":str(datetime.datetime(2014, 10, 6, 0, 0)),
                  "note":"I went here with Leyna to see Torrey's Peak. Lot's of water. Cool mine stuff for melting things. "})
    ibeen.append({"id":17,
                  "type": "been_there",
                  "last_time":str(datetime.datetime(2014, 8, 25, 0, 0)),
                  "note":"Gets us to Jenny Creek. Pretty place. Went once with Kyle and the last time with the Girls."})
    ibeen.append({"id":19,
                  "type": "been_there",
                  "last_time":str(datetime.datetime(2014, 8, 25, 0, 0)),
                  "note":"Gets us to Jenny Creek. Pretty place. Went once with Kyle and the last time with the Girls."})
    ibeen.append({"id":424,
                  "type": "been_there",
                  "last_time":str(datetime.datetime(2014, 8, 27, 0, 0)),
                  "note":"Drove around here with Dad. Some fun bumps, and looks like there are cool places to camp. "})
    ibeen.append({"id":250,
                  "type": "been_there",
                  "last_time":str(datetime.datetime(2014, 9, 24, 0, 0)),
                  "note":"Went here with Amanda, takes you to the top of a mountain next to Keystone ski lifts. There was a cave in the rock. More mines at sunset."})
    ibeen.append({"id":377,
                  "type": "been_there",
                  "last_time":str(datetime.datetime(2014, 10, 4, 0, 0)),
                  "note":"Went here with Abby and Amanda to see Wild Irishman mine stuff. Drove through a pond. Need to do Hunkidori Mine."})
    ibeen.append({"id":158,
                  "type": "been_there",
                  "last_time":str(datetime.datetime(2014, 9, 1, 0, 0)),
                  "note":"Ron told me about this one and how it gets to Rampart Range. Me and Crissy went this way to get back home."})
    ibeen.append({"id":222,
                  "type": "been_there",
                  "last_time":str(datetime.datetime(2014, 8, 31, 0, 0)),
                  "note":"Fun roller coaster place I took the girls. Lot's of rolling stuff."})
    ibeen.append({"id":234,
                  "type": "been_there",
                  "last_time":str(datetime.datetime(2014, 10, 16, 0, 0)),
                  "note":"Went with Dad and James after seeing Keen's place. James meets Jeep for first time. Banged up my bottom a lot."})

    ibeen.append({"id":20,
                  "type": "been_there",
                  "last_time":str(datetime.datetime(2014, 10, 27, 0, 0)),
                  "note":"Went with Liz and Abby, lots of Barhite history."})

    #Places I need to warn about
    ibeen.append({"id":6,
                  "type": "warning",
                  "last_time":str(datetime.datetime(2014, 8, 21, 0, 0)),
                  "note":"Looks like the floods wrecked this."})
    ibeen.append({"id":200,
                  "type": "warning",
                  "last_time":str(datetime.datetime(2014, 8, 31, 0, 0)),
                  "note":"Tried going here with Amanda. A gate was shut and a truck was coming out. Looked like construction."})


    #Places not in trail damage
    iadded.append({"id":10001,
                   "ibeen_there": "i_added",
                   "my_last_time":str(datetime.datetime(2014, 8, 31, 0, 0)),
                   "my_note":"Went through here with Crystal. Getting in was the most sketchy part, have to go down gnarly path. Pretty and several interesting networks.",
                   "trail_type" : "Straight Through",
                   "updated" : str(datetime.datetime(2014, 9, 1, 0, 0)),
                   "elevation" : [0,0],
                   "name" : "Beaver Creek Rd",
                   "trail_length" : 0,
                   "nearby_trails" : ["don't know"],
                   "county" : "don't know",
                   "lat_lng" : [39.057322, -104.991560],
                   "nearby_towns" : ["Monument","Woodland Park"],
                   "directions" : "up in the hills",
                   "legend" : { "scenery": 2,
                                "elevation" : 3,
                                "playgrounds" : 2,
                                "low_rating" : 3,
                                "high_rating" : 3,
                                "climbs_descents" : 4,
                                "dirt_mud" : 3,
                                "cliffs_ledges" : 1,
                                "rock_crawling" : 2,
                                "water_crossing" :2
                                }
                   })
    iadded.append({"id":10002,
                   "ibeen_there": "i_added",
                   "my_last_time":str(datetime.datetime(2014, 10, 6, 0, 0)),
                   "my_note":"Almost got blown off me Jeep here. Leyna almost died from fear--she cried.",
                   "trail_type" : "Out and Back",
                   "updated" : str(datetime.datetime(2014, 10, 6, 0, 0)),
                   "elevation" : [0,13,000],
                   "name" : "Pictures with Torrey's Peak",
                   "trail_length" : 0,
                   "nearby_trails" : ["don't know"],
                   "county" : "don't know",
                   "lat_lng" : [39.655585, -105.776072],
                   "nearby_towns" : ["George Town"],
                   "directions" : "Turn onto dirt from Guanella Pass",
                   "legend" : { "scenery": 5,
                                "elevation" : 5,
                                "playgrounds" : 3,
                                "low_rating" : 3,
                                "high_rating" : 5,
                                "climbs_descents" : 3,
                                "dirt_mud" : 3,
                                "cliffs_ledges" : 5,
                                "rock_crawling" : 3,
                                "water_crossing" :4
                                }
                   })
    iadded.append({"id":10003,
                   "ibeen_there": "i_added",
                   "my_last_time":str(datetime.datetime(2014, 9, 24, 0, 0)),
                   "my_note":"Found cool cave here.",
                   "trail_type" : "Out and Back",
                   "updated" : str(datetime.datetime(2014, 9, 24, 0, 0)),
                   "elevation" : [0,14,000],
                   "name" : "Indiana Amanda",
                   "trail_length" : 0,
                   "nearby_trails" : ["don't know"],
                   "county" : "don't know",
                   "lat_lng" : [39.556805, -105.916962],
                   "nearby_towns" : ["Keystone"],
                   "directions" : "",
                   "legend" : { "scenery": 5,
                                "elevation" : 5,
                                "playgrounds" : 1,
                                "low_rating" : 3,
                                "high_rating" : 3,
                                "climbs_descents" : 3,
                                "dirt_mud" : 1,
                                "cliffs_ledges" : 5,
                                "rock_crawling" : 2,
                                "water_crossing" :1
                                }
                   })

    iadded.append({"id":10004,
                   "ibeen_there": "i_added",
                   "my_last_time":str(datetime.datetime(2014, 10, 4, 0, 0)),
                   "my_note":"Cool cabins left here from the 1860s.",
                   "trail_type" : "Out and Back",
                   "updated" : str(datetime.datetime(2014, 10, 4, 0, 0)),
                   "elevation" : [0,14,000],
                   "name" : "Wild Irishman Mines",
                   "trail_length" : 0,
                   "nearby_trails" : ["don't know"],
                   "county" : "don't know",
                   "lat_lng" : [39.5588860168546, -105.88752329349518],
                   "nearby_towns" : ["Keystone"],
                   "directions" : "",
                   "legend" : { "scenery": 5,
                                "elevation" : 5,
                                "playgrounds" : 1,
                                "low_rating" : 3,
                                "high_rating" : 3,
                                "climbs_descents" : 3,
                                "dirt_mud" : 2,
                                "cliffs_ledges" : 3,
                                "rock_crawling" : 3,
                                "water_crossing" :3
                                }
                   })

    iadded.append({"id":10005,
                   "ibeen_there": "i_added",
                   "my_last_time":str(datetime.datetime(2014, 9, 28, 0, 0)),
                   "my_note":"Cool mine above George Town, I first went to with Liz and Crystal.",
                   "trail_type" : "Out and Back",
                   "updated" : str(datetime.datetime(2014, 9, 28, 0, 0)),
                   "elevation" : [0,14,000],
                   "name" : "Mine above George Town",
                   "trail_length" : 0,
                   "nearby_trails" : ["don't know"],
                   "county" : "don't know",
                   "lat_lng" : [39.719805099872154, -105.71597993373871],
                   "nearby_towns" : ["Empire","George Town"],
                   "directions" : "Go to Empire, turn left",
                   "legend" : { "scenery": 5,
                                "elevation" : 3,
                                "playgrounds" : 1,
                                "low_rating" : 3,
                                "high_rating" : 3,
                                "climbs_descents" : 3,
                                "dirt_mud" : 2,
                                "cliffs_ledges" : 2,
                                "rock_crawling" : 3,
                                "water_crossing" :1
                                }
                   })

    iadded.append({"id":10006,
                   "ibeen_there": "i_added",
                   "my_last_time":str(datetime.datetime(2014, 8, 3, 0, 0)),
                   "my_note":"Family photos of Barhites here. My first 4wheeling adventure.",
                   "trail_type" : "Out and Back",
                   "updated" : str(datetime.datetime(2014, 8, 3, 0, 0)),
                   "elevation" : [0,14,000],
                   "name" : "Bill Moore Lake Pictures",
                   "trail_length" : 0,
                   "nearby_trails" : ["don't know"],
                   "county" : "don't know",
                   "lat_lng" : [39.80444305945172, -105.71160793304443],
                   "nearby_towns" : ["Empire"],
                   "directions" : "Go to Empire, turn right",
                   "legend" : { "scenery": 5,
                                "elevation" : 4,
                                "playgrounds" : 3,
                                "low_rating" : 4,
                                "high_rating" : 6,
                                "climbs_descents" : 4,
                                "dirt_mud" : 2,
                                "cliffs_ledges" : 2,
                                "rock_crawling" : 4,
                                "water_crossing" :1
                                }
                   })

    iadded.append({"id":10007,
                   "ibeen_there": "i_added",
                   "my_last_time":str(datetime.datetime(2014, 10, 17, 0, 0)),
                   "my_note":"Cool old train tunnel I went through with Dad and James.",
                   "trail_type" : "Straight Through",
                   "updated" : str(datetime.datetime(2014, 10, 17, 0, 0)),
                   "elevation" : [0,14,000],
                   "name" : "Upper Gold Camp Road",
                   "trail_length" : 0,
                   "nearby_trails" : ["don't know"],
                   "county" : "don't know",
                   "lat_lng" : [38.73184929526226, -105.02583146095276],
                   "nearby_towns" : ["Broadmore","Cripple Creek"],
                   "directions" : "Go through Broadmore",
                   "legend" : { "scenery": 4,
                                "elevation" : 3,
                                "playgrounds" : 1,
                                "low_rating" : 1,
                                "high_rating" : 1,
                                "climbs_descents" : 1,
                                "dirt_mud" : 1,
                                "cliffs_ledges" : 3,
                                "rock_crawling" : 1,
                                "water_crossing" :1
                                }
                   })

    iadded.append({"id":10008,
                   "ibeen_there": "i_added",
                   "my_last_time":str(datetime.datetime(2014, 10, 27, 0, 0)),
                   "my_note":"Start of Switzerland Trail.",
                   "trail_type" : "Straight Through",
                   "updated" : str(datetime.datetime(2014, 10, 27, 0, 0)),
                   "elevation" : [0,14,000],
                   "name" : "Switzerland Trail from Ward",
                   "trail_length" : 0,
                   "nearby_trails" : ["don't know"],
                   "county" : "don't know",
                   "lat_lng" : [40.054605032933466, -105.49516439437866],
                   "nearby_towns" : ["Ward"],
                   "directions" : "Start at Ward",
                   "legend" : { "scenery": 4,
                                "elevation" : 2,
                                "playgrounds" : 1,
                                "low_rating" : 1,
                                "high_rating" : 1,
                                "climbs_descents" : 1,
                                "dirt_mud" : 1,
                                "cliffs_ledges" : 4,
                                "rock_crawling" : 1,
                                "water_crossing" :1
                                }
                   })

    iadded.append({"id":10009,
                   "ibeen_there": "i_added",
                   "my_last_time":str(datetime.datetime(2014, 10, 27, 0, 0)),
                   "my_note":"End of Switzerland Trail.",
                   "trail_type" : "Straight Through",
                   "updated" : str(datetime.datetime(2014, 10, 27, 0, 0)),
                   "elevation" : [0,14,000],
                   "name" : "Switzerland Trail from Ward",
                   "trail_length" : 0,
                   "nearby_trails" : ["don't know"],
                   "county" : "don't know",
                   "lat_lng" : [40.0178209295147, -105.50934791564941],
                   "nearby_towns" : ["Ward"],
                   "directions" : "Start at Ward",
                   "legend" : { "scenery": 4,
                                "elevation" : 2,
                                "playgrounds" : 1,
                                "low_rating" : 1,
                                "high_rating" : 1,
                                "climbs_descents" : 1,
                                "dirt_mud" : 1,
                                "cliffs_ledges" : 4,
                                "rock_crawling" : 1,
                                "water_crossing" :1
                                }
                   })

         

              

    PATH = os.path.abspath(os.path.dirname(__file__))
    cherrypy.tree.mount(Root(sdat,ibeen,iadded), '/', config={
        '/': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': PATH,
                'tools.staticdir.index': 'index.html',
            },
    })

    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    main()
