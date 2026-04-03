#! /bin/bash
[[ $EUID -ne 0 ]] && echo 'Error: This script must be run as root!' && exit 1
#closed syslog
#systemctl stop syslog.service
#systemctl disable syslog.service
#systemctl stop syslog.socket
#systemctl disable syslog.socket
#check 

variablename=(deepin-defender x11-apps)
for data in ${variablename[@]}
do
       echo ${data}
       a=`apt-cache policy ${data}|grep "已安装：" |awk '{print $1}'`
       if [ ! -n "$a" ];then
        echo "未发现${data}版本"
               else
              echo "当前系统安装版本：$a"
       fi
done

# https://www.cnblogs.com/cobbliu/p/5389556.html
# 总内存的最大百分比，系统所能拥有的最大脏页缓存的总量 60
a=`cat /proc/sys/vm/dirty_ratio`
# 35 如果需要把缓存持续的而不是一下子大量的写入硬盘，降低这个值
b=`cat /proc/sys/vm/dirty_background_ratio`
# 4096 这个参数对顺序读非常有用,意思是,一次提前读多少内容,无论实际需要多少.默认一次读 128kb 远小于要读的,设置大些对读大文件非常有用,可以有效的减少读 seek 的次数,这个参数可以使用 blockdev –setra 来设置,setra 设置的是多少个扇区,所以实际的字节是除以2,比如设置 512 ,实际是读 256 个字节
pp=`cat /sys/block/sda/queue/read_ahead_kb` 
if [ $? == 0 ]
    then
c=$pp
    else
    c=`cat /sys/block/nvme0n1/queue/read_ahead_kb`
fi
# 128 请求队列的长度。默认可以接受128个请求
pl=`cat /sys/block/sda/queue/nr_requests`
if [ $? == 0 ]
    then
d=$pl
    else
    d=`cat /sys/block/nvme0n1/queue/nr_requests`
fi



#cho $a--- $b---- $c ---$d
if [ $a == 60 ] 
then
	echo PASS
else
	echo FAIL  dirty_ratio $a != 60
	exit
	fi
if [ $b == 35 ] 
then
	echo PASS
else
	echo FAIL  dirty_background_ratio $b != 35
	exit
	fi
if [ $c == 4096 ] 
then
	echo PASS
else
	echo FAIL read_ahead_kb $c != 4096
	exit
	fi
if [ $d == 128 ] 
then


	echo PASS
else
	echo FAIL nr_requests $d != 128
	exit
	fi
#unload 
#echo y | apt autoremove deepin-system-monitor 
#echo y | apt autoremove deepin-log-viewer



