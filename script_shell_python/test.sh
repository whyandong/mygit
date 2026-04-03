#! /bin/bash
while true
do
DATE=$(date +"%Y-%m-%d %H:%M:%S")
if ping -c 1 10.20.22.124 >/dev/null
# if [ $? -eq 0 ]
 then
	echo yes
 else 
	echo "no! $DATE " >> ./ping.log
fi
done 
