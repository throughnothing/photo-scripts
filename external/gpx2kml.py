#!/usr/bin/python
#
# Copyright (c) 2007 Brian "Beej Jorgensen" Hall
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys
import os.path
import xml.dom.minidom

symbolMap = {
	"Dot":"wpt_dot",
	"Amusement Park":"amuse_pk",
	"Ball Park":"ball",
	"Bank":"dollar",
	"Bar":"mug",
	"Campground":"camp",
	"Large City":"lrg_cty",
	"Medium City":"med_cty",
	"Small City":"sml_cty",
	"Convenience Store":"gas_plus",
	"Danger Area":"skull",
	"Dangerous Area":"danger",
	"Department Store":"store",
	"Drinking Water":"drinking_wtr",
	"Fast Food":"fastfood",
	"Fishing Area":"fish",
	"Fitness Center":"fitness",
	"Gas Station":"fuel",
	"Glider Area":"glider",
	"Mine":"mine",
}

class AppInfo:
	def __init__(self, argv):
		self.scriptname = os.path.basename(argv.pop(0))
		self.outfilename = None
		self.infilename = None

		self.infile = None
		self.outfile = None

		while len(argv) > 0:
			if argv[0] == "-h" or argv[0] == "--help" or argv[0] == "-?":
				self.usageExit()

			elif argv[0] == "-o":
				argv.pop(0)
				if len(argv) == 0: self.usageExit()
				self.outfilename = argv[0]

			elif self.infilename == None:
				self.infilename = argv[0]

			argv.pop(0)

		if self.infilename == None:
			self.infile = sys.stdin
			self.infilename = "<stdin>"
		else:
			try:
				self.infile = file(self.infilename, "r")
			except IOError, (no, str):
				self.errorExit("error opening %s: %s" % \
					(self.infilename, str), 2)

		try:
			self.dom = xml.dom.minidom.parse(self.infile)
		except Exception, (str):
			self.errorExit("%s: %s" % (self.infilename, str), 4)

		if self.outfilename == None:
			self.outfile = sys.stdout
			self.outfilename = "<stdout>"
		else:
			try:
				self.outfile = file(self.outfilename, "w")
			except IOError, (no, str):
				self.errorExit("error opening %s: %s" % \
					(self.outfilename, str), 3)

	def __del__(self):
		if self.infile != None: self.infile.close()
		if self.outfile != None: self.outfile.close()

	def errorExit(self, str, status=1):
		sys.stderr.write("%s: %s\n" % (self.scriptname, str))
		sys.exit(status)
		
	def usageExit(self):
		sys.stderr.write("usage: %s [-o outfile] [infile]\n" % self.scriptname)
		sys.exit(1)

def getTextBelow(node, subnodename, handleNone=False):
	subnodes = node.getElementsByTagName(subnodename)
	if subnodes != []:
		return subnodes[0].firstChild.data
	
	if handleNone: return ""

	return None
		
def symTranslate(name):
	if not symbolMap.has_key(name): name = "Dot"
	return symbolMap[name]

def main(argv):
	ai = AppInfo(argv)

	gpx = ai.dom.firstChild

	waypoints = gpx.getElementsByTagName("wpt")

	ai.outfile.write("""<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated by gpx2kml -->
<kml xmlns="http://earth.google.com/kml/2.1">
\t<Document>
\t\t<Style id="trackStyle">
\t\t\t<LineStyle>
\t\t\t\t<color>7fff0000</color>
\t\t\t\t<width>4</width>
\t\t\t</LineStyle>
\t\t</Style>
""")

	if waypoints != []:
		for wp in waypoints:
			lat = wp.getAttribute("lat")
			lon = wp.getAttribute("lon")
			name = getTextBelow(wp, "name", True)
			sym = getTextBelow(wp, "sym")
			desc = getTextBelow(wp, "desc")
			ele = getTextBelow(wp, "ele")

			ai.outfile.write('\t\t<Placemark>\n')
			ai.outfile.write('\t\t\t<name>%s</name>\n' % name)
			if desc != '' and desc != None:
				ai.outfile.write('\t\t\t<description>%s</description>\n' \
					% desc)
			ai.outfile.write("\t\t\t<styleUrl>#trackStyle</styleUrl>\n")
			ai.outfile.write('\t\t\t<Point>\n')
			ai.outfile.write('\t\t\t\t<coordinates>')
			ai.outfile.write('%s,%s</coordinates>\n' % (lon, lat))
			ai.outfile.write('\t\t\t</Point>\n')

			ai.outfile.write('\t\t</Placemark>\n')

	tracks = gpx.getElementsByTagName("trk")

	if tracks != []:
		for trk in tracks:

			name = getTextBelow(trk, "name", True)
			desc = getTextBelow(trk, "desc")

			ai.outfile.write('\t\t<Placemark>\n')
			ai.outfile.write('\t\t\t<name>%s</name>\n' % name)
			if desc != '' and desc != None:
				ai.outfile.write('\t\t\t<description>%s</description>\n' \
					% desc)
			ai.outfile.write("\t\t\t<styleUrl>#trackStyle</styleUrl>\n")
			ai.outfile.write("\t\t\t<LineString>>\n")
			ai.outfile.write("\t\t\t\t<coordinates>\n")

			for seg in trk.getElementsByTagName("trkseg"):
				for trkpt in seg.getElementsByTagName("trkpt"):
					lat = trkpt.getAttribute("lat")
					lon = trkpt.getAttribute("lon")
					ele = getTextBelow(trkpt, "ele")

					ai.outfile.write("\t\t\t\t\t%s,%s\n" % (lon, lat))

			ai.outfile.write("\t\t\t\t</coordinates>\n")
			ai.outfile.write("\t\t\t</LineString>>\n")
			ai.outfile.write('\t\t</Placemark>\n')
	
	ai.outfile.write('\t</Document>\n')
	ai.outfile.write('</kml>\n')

	return 0

if __name__ == "__main__": sys.exit(main(sys.argv))
