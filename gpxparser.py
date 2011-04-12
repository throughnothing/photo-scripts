# This file is mostly code from gpx2kml.py
# need to run script setting PYTHONPATH= to point to travel package directory
# My travel module for travel site, TrackPoint is a mongoengine Document object
from travel.model import TrackPoint

import sys
import os.path
import xml.dom.minidom
from datetime import datetime

from mongoengine import connect

connect('travel', host='localhost', port=27017)

def usage():
    print "gpxparser gpxfile.gpx"

def getTextBelow(node, subnodename, handleNone=False):
	subnodes = node.getElementsByTagName(subnodename)
	if subnodes != []:
		return subnodes[0].firstChild.data
	
	if handleNone: return ""

	return None

def main(argv):
    #if len(argv < 2): usage()

    gpxfile = argv[1]
    dom = xml.dom.minidom.parse(gpxfile)
    gpx = dom.firstChild

    # Don't care about these for now
    waypoints = gpx.getElementsByTagName("wpt")
    # Care about these
    tracks = gpx.getElementsByTagName("trk")

    if tracks != []:
        for trk in tracks:
            name = getTextBelow(trk, "name", True)
            desc = getTextBelow(trk, "desc")

            for seg in trk.getElementsByTagName("trkseg"):
                for trkpt in seg.getElementsByTagName("trkpt"):
                    lat = float(trkpt.getAttribute("lat"))
                    lon = float(trkpt.getAttribute("lon"))
                    ele = float(getTextBelow(trkpt, "ele"))
                    ts = getTextBelow(trkpt, "time")
                    dts = datetime.strptime(ts,'%Y-%m-%dT%H:%M:%SZ')

                    m_trkpt = TrackPoint(date=dts,location= [lat,lon],altitude=ele)
                    m_trkpt.save()

if __name__ == "__main__": 
    sys.exit(main(sys.argv))
