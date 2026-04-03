#!/bin/bash

while [ 1 ];
do
xdotool getmouselocation|sed 's/x:\([0-9]\+\)[ \t]y:\([0-9]\+\)[ \t].*/\1;\2/'
done
