#!/bin/bash

# $1 = directory to .gpx file(s)
# $2 = directory of photos
# $3 = seconds time offset where camera time + seconds = GMT
#		(defaults to 14400 which will adjust for EST during daylight savings)

if [[ ! -n "$1" ]]; then
	echo "Usage: $0 [.gpx directory] [photo directory]"
	exit 0;
fi

if [[ ! -n "$2" ]]; then
	echo "Usage: $0 [.gpx directory] [photo directory]"
	exit 0;
fi

TIMEOFFSET=$2
if [[ ! -n "$2" ]]; then
	echo "Defaulting time offset to 0..."
	TIMEOFFSET=0
fi

gpsPhoto.pl --gpsdir $1 --dir $2 --maxtimediff 900 --timeoffset $TIMEOFFSET

