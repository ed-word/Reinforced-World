#!/bin/bash
EXPECTED_ARGS=1
E_BADARGS=65

if [ $# -lt $EXPECTED_ARGS ]
then
  echo "Usage: `basename $0` video frames/sec"
  exit $E_BADARGS
fi

FRAMES=$1

BASE_DIR=$(pwd)/angelapp/modules/classification

echo $BASE_DIR

for file in $(pwd)/angelapp/modules/classification/Data/*
do

NAME=${file%.*}
BNAME=`basename $NAME`
echo $BNAME
mkdir -p -m 755 $(pwd)/angelapp/modules/classification/Data/Extraction/

ffmpeg -i $file -r $FRAMES $(pwd)/angelapp/modules/classification/Data/Extraction/$BNAME.%4d.jpg

done