#!/bin/bash

function usb_rw(){
	for (( i=1;i<4;i++ ))
	do
	sync&&echo 3  > /proc/sys/vm/drop_caches
	sleep 1
	dd if=/dev/zero of=test.img bs=100M count=12
	sleep 1
	sync&&echo 3  > /proc/sys/vm/drop_caches
	sleep 1
	dd if=test.img of=/dev/null bs=100M count=12 
	sleep 1
	rm -rf ./test.img
	done
}

usb_rw >> /home/uos/usb.log 2>&1
echo -e "\n\n\n" >> /home/uos/usb.log 2>&1
python3 usbData.py