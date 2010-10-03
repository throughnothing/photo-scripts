#!/bin/bash

# $1 = directory to .gpx file + photos

if [[ ! -n "$1" ]]; then
	echo "Usage: $0 [directory]"
	exit 0;
fi

gpsPhoto.pl --gpsdir $1 --dir $1 --maxtimediff 60 --timeoffset 14400

