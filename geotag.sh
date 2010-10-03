#!/bin/bash

# $1 = directory to .gpx file + photos
# $2 = seconds time offset where camera time + seconds = GMT
#		(defaults to 14400 which will adjust for EST during daylight savings)

if [[ ! -n "$1" ]]; then
	echo "Usage: $0 [directory]"
	exit 0;
fi

TIMEOFFSET=$2
if [[ ! -n "$2" ]]; then
	TIMEOFFSET=14400
fi

gpsPhoto.pl --gpsdir $1 --dir $1 --maxtimediff 60 --timeoffset $TIMEOFFSET

