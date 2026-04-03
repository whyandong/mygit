#!/bin/bash
#访问端口配置
orc_port=1522
msql_port=3306
mid_port=15385
#  配置脚本存放路径
script="/usr/local/AlarmTp"
count=1
# 100 定义循环次数上限 可自定义
while [ $count -lt 100 ]
#单次循环时间间隔（秒）可自定义
sleep 2
do
#访问服务器IP
orc_ip=192.168.1.192
msql_ip=192.168.1.192
mid_ip=192.168.1.71
#ping包
 i6=`/usr/bin/ping -c 1 $orc_ip | grep "packet loss" | awk '{print $8}'`
 echo "$i6"
 i7=`/usr/bin/ping -c 1 $msql_ip | grep "packet loss" | awk '{print $8}'`
 echo "$i7"
 i8=`/usr/bin/ping -c 1 $mid_ip | grep "packet loss" | awk '{print $8}'`
 echo "$i8"
if [ "$i6" == "100%" ] || [ "$i7" == "100%" ] || [ "$i8" == "100%" ]; then
  echo "继续循环，当前循环次数$count"
 else
#确保端口号开启
  b1=`/usr/bin/nmap -sT $orc_ip -p $orc_port | grep $orc_port | awk '{printf $2}'`
  echo "$b1"
  b2=`/usr/bin/nmap -sT $msql_ip -p $msql_port | grep $msql_port | awk '{printf $2}'`
  echo "$b2"
  b3=`/usr/bin/nmap -sT $mid_ip -p $mid_port | grep $mid_port | awk '{printf $2}'`
  echo "$b3"
  if [ "$b1" == "open" ] && [ "$b2" == "open" ] && [ "$b3" == "open" ]; then
#调用脚本启动系统组件
  echo "正在启动脚本，请稍后"
  sleep 2
 su - zhdev -lc "cd $script && ./run.sh"
  break
else
   echo "端口未开启"
  fi
 fi
count=`expr $count + 1`
done

