#!/bin/bash

KML_PATH='/home/throughnothing/projects/throughnothing.com/travel/kml'

TS=`date +'%Y-%m-%d--%H:%M:%S'`
if [ -z $1 ]; then
  FILE=$TS
else
  FILE=$1 
fi

sudo gpsbabel -t -i garmin -f usb: -o kml -F $KML_PATH/$FILE.kml
sudo gpsbabel -t -i garmin -f usb: -o gpx -F /tmp/$FILE.gpx
