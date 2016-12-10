#!/bin/sh

while true;
do
    ping -c1 192.168.43.157
    if [ $? -eq 0 ]
    then
       python /home/pi/Desktop/rmmf/raspberrypi/hx711py/obol.py
	exit 0
    fi
    done


