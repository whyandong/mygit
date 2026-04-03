#! /bin/bash
times=20
for i in $(seq 1 $times)
do
	printf "the $i time of s4 sleep...\n"
	sleep 60
	echo reboot > /sys/power/disk && echo disk > /sys/power/state
	printf "the $i time wake up from s4 sleep\n\n\n"
done
