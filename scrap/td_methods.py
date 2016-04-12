import requests
from xml.etree import ElementTree
from bs4 import BeautifulSoup
from xml.etree import ElementTree
import re

def grab_trails_colorado(req):
    """Grabs all of the trails with IDs into the pages

    """
    tree = ElementTree.fromstring(req.content)
    trails = []
    for marker in tree:
        d = {}
        for name, value in marker.attrib.items():
            d[name] = value
        trails.append(d)

    return trails

def grab_traildamage_page_info(req):
    """Scarps information from each page
    """
    soup = BeautifulSoup(req.content)

    td = soup.findAll('td', {'class':'legend'})
    trs = td[0].findAll('tr')

    d = {}
    for tr in trs:
        tds = tr.findAll('td')
        try:
            rname =  tds[0].findAll('b')[0].contents
            if rname[0] == 'Low-End Rating:':
                d[rname[0]] = int(tds[1].findAll('b')[0].contents[0])
            elif rname[0] == 'High-End Rating:':
                d[rname[0]] = int(tds[1].findAll('b')[0].contents[0])
            elif rname[0] == 'Rock Crawling:':
                d[rname[0]] = len(tds[1].findAll('img'))
            elif rname[0] == 'Dirt & Mud:':
                d[rname[0]] = len(tds[1].findAll('img'))
            elif rname[0] == 'Water Crossings:':
                d[rname[0]] = len(tds[1].findAll('img'))
            elif rname[0] == 'Playgrounds:':
                d[rname[0]] = len(tds[1].findAll('img'))
            elif rname[0] == 'Cliffs & Ledges:':
                d[rname[0]] = len(tds[1].findAll('img'))
            elif rname[0] == 'Climbs & Descents:':
                d[rname[0]] = len(tds[1].findAll('img'))
            elif rname[0] == 'Elevation:':
                d[rname[0]] = len(tds[1].findAll('img'))
            elif rname[0] == 'Scenery:':
                d[rname[0]] = len(tds[1].findAll('img'))
            elif rname[0] == 'Other Activities:':
                d[rname[0]] = len(tds[1].findAll('img'))
            elif rname[0] == 'Other Activities:':
                d[rname[0]] = len(tds[1].findAll('img'))
        except:
            pass

    pars = soup.findAll("p")
    pdat = {}
    pdate = {}
    for n,p in enumerate(pars):

        #Get head stuff
        if n == 0:
            pdat["TrailName"] = p.contents[0].text
            pdat["Location"] = p.contents[1].text

        if n == 1:

            sts = p.text.split('\n')

            for el in sts:
                p = re.compile(r'Roads:\s*(.*)')
                res = p.search(el)
                if res:
                    try:
                        g = res.groups()[0].split(",")
                        pdat["ForestServiceRoads"] = g
                    except Exception as e:
                        pdat["ForestServiceRoads"] = str(e)
        
                p = re.compile(r'Type:\s*(.*)')
                res = p.search(el)
                if res:
                    try:
                        g = res.groups()[0]
                        pdat["TrailType"] = g
                    except Exception as e:
                        pdat["TrailType"] = str(e)
        
                p = re.compile(r'Towns:\s*(.*)')
                res = p.search(el)
                if res:
                    try:
                        g = res.groups()[0]
                        pdat["NearbyTowns"] = g.split(',')
                    except Exception as e:
                        pdat["NearbyTowns"] = str(e)
        
                p = re.compile(r'Trails:\s*(.*)')
                res = p.search(el)
                if res:
                    try:
                        g = res.groups()[0]
                        pdat["NearbyTrails"] = g.split(',')
                    except Exception as e:
                        pdat["NearbyTrails"] = str(e)

                p = re.compile(r'Length:\s*(.*)')
                res = p.search(el)
                if res:
                    try:
                        g = res.groups()[0]
                        pdat["TrailLength"] = g
                    except Exception as e:
                        pdat["TrailLength"] = str(e)
      
                p = re.compile(r'Elevation:\s*(.*)')
                res = p.search(el)
                if res:
                    try:
                        g = res.groups()[0]
                        pdat["Elevation"] = g
                    except Exception as e:
                        pdat["Elevation"] = str(e)

        if n == 2:
             pdate["description"] = p.text
        
        if n == 3:
             pdate["updated"]   = p.text

        if n == 7:
             pdate["directions"] = p.text
  
    pdat["legend"] = d

    pdate["info"] = pdat

    return pdate

if __name__ == "__main__":

    r = requests.get("http://www.traildamage.com/trails/index.php?id=326")

    d = grab_traildamage_page_info(r)

    a = raw_input()