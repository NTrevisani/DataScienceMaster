#!/bin/bash
#!/usr/bin/env python

COST=$1

ALPHA=$2

shots_list="1 2 4 6 8 10 12 16 20 24 32"

for shot in $shots_list; do

    echo python3.7 scan_script.py $shot $COST $ALPHA \&
    #python3.7 scan_script.py $shot $COST $ALPHA \&
    
done

