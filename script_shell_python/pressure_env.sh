#! /bin/bash
[[ $EUID -ne 0 ]] && echo 'Error: This script must be run as root!' && exit 1
#磁盘占用比例配置
bili=8 #增加该值可以增加磁盘占用率 建议8 , 7为90%
check_err(){
	if [ $? != 0 ]
        then
  		echo  dd option Fail ...
	      	exit 2	
        else
               echo check env Pass ...
        fi
}

size1=`df -hT / |awk '{print $5}' | grep G | awk  '{printf substr($1,1,1)}'`
size2=`expr $size1 / $bili  `
size3=`expr $size2 \* 60 `
#size3=${size1#*.}
echo $size3
check_err
echo / path press take up 80% loading  ....  creat filesize $size2
dd if=/dev/zero of=/testfile bs=100M count=$size3
check_err
sleep 10

echo  cpu press loading ..... 
sleep 2
#for i in `seq 2 $(cat /proc/cpuinfo |grep "physical id" |wc -l)`; do dd if=/dev/zero of=/dev/null & done
apt update && apt install stress
#默认将CPU核70%压满,持续2小时
stress -c 3 -t 7200 &

check_err

echo mem press loading .....
#默认内存占用60%,持续2小时,仅针对用户态
stress --vm 8 --vm-bytes 512M --vm-hang 80 --timeout 7200s &
check_err

sleep 7500
echo evn timeuot ... restore env  loading ...
rm -rf /testfile
kill -9 `ps -ef | grep "vm" | awk '{print $2}'`
kill -9 `ps -ef | grep "stress" | awk '{print $2}'`
sleep 2
echo done !!


#b=1
#a=`cat ./times.log`
#if [[ $a -gt $count ]] 
# then
#	echo restore env loading .....
#	sleep 2
#	kill all `ps -ef|grep "dd if=/dev/zero of=/dev/null" | awk '{print $2}'`
#	rm -rf  /testfile
#	rm -rf  /file_file
#	exit 2
#else 
#	ct=`expr $a + $b`
#	echo "$ct" > ./times.log
#	echo env done , show your testcase !
#	mkdir /tmp/memory
#	mount -t tmpfs -o size=1024M tmpfs /tmp/memory
#	dd if=/dev/zero of=/tmp/memory/block
#	sleep 3600
#	rm /tmp/memory/block
#	umount /tmp/memory
#	rmdir /tmp/memory
#fi
