#! /bin/bash 
[[ $EUID -ne 0 ]] && echo 'Error: This script must be run as root!' && exit 1
DATE=$(date +"%Y-%m-%d-%H:%M:%S")
apt install -y lm-sensors
while true ; do echo "$DATE DISK:"  >> ./monitor_temp.log &&  smartctl --all /dev/nvme0 | grep "Temperature:" >> ./monitor_temp.log && sensors >> ./monitor_temp.log; sleep 60 ; done &tail -f ./monitor_temp.log

