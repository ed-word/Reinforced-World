#!/bin/bash
echo $PWD
sh ./angelapp/modules/classification/extract_frames.sh 20

python3 ./angelapp/modules/classification/Resize.py

python3 ./angelapp/modules/classification/Car_Crash_inference.py

exit
