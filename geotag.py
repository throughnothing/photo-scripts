#!/usr/bin/python
import sys, os, commands

BASE_PHOTO_DIR="/home/throughnothing/Pictures/Photos"
BASE_KML_DIR="/home/throughnothing/projects/throughnothing.com/travel/kml"

def usage():
  print "%s [.gpx directory]" % (sys.argv[0])

if len(sys.argv) < 2:
  usage() 


gps_dir = os.path.abspath(sys.argv[1])

files = os.listdir(gps_dir)
for file in files:
  year  = file[0:4]
  month = file[4:6]
  day   = file[6:8]

  gps_file = "/".join([gps_dir,file])

  photo_dir = "/".join([BASE_PHOTO_DIR ,year,month,day])
  
  result = commands.getstatusoutput(
    'gpsPhoto.pl --gpsfile "%s" --dir "%s" --maxtimediff 900 --timeoffset 0'
    % ( gps_file, photo_dir )
  )
  print result[1].split('\n')[-1]

  #Convert .gpx to .kml and put in right place
  kml_file = "/".join([BASE_KML_DIR,'-'.join([year,month,day])]) + '.kml'
  result = commands.getstatusoutput(
    './external/gpx2kml.py "%s" >> "%s"' 
    % ( gps_file, kml_file )
  )


  

  
