#!/bin/bash

sh extract_frames.sh 20

python3 Resize.py

python3 Car_Crash_inference.py

exit
