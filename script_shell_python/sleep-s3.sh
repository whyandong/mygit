#!/bin/bash
# 先rtcwake > wakealarm时钟 > 网络唤醒
check_rtc=`cat /sys/class/rtc/rtc0/device/power/wakeup`
wakealarm_path=/sys/class/rtc/rtc0/wakealarm
wakeonlan=`ethtool $2 | grep wake-on`
NUM=$1



if [ $('whoami') != 'root' ];then
  echo "请使用root用户执行！！!"; >> s3.log
  sleep 1
  exit
fi


判断命令是否执行成功
function is_success(){
 	if [[ $? -ne 0 ]]; then
 		echo "$1失败" >> s3.log
 		exit
 	else
 		echo "$1成功" >> s3.log
 	fi
 }



if [[ $check_rtc == "enabled" ]]; then

    echo "尝试rtcwake方式测试" >> s3.log
    while [ $NUM -gt 0 ]
    do
    	cnum=`expr $1 - $NUM + 1`
    	echo "将进行  第 $cnum 次休眠" >> s3.log
    	sleep 3
    	rtcwake -m mem -s 30
        is_success "rtcwake测试" >> s3.log
    	NUM=`expr $NUM - 1`
    done

else
    echo "该机器不支持rtcwake自动唤醒功能" >> s3.log
    if [[ -f $wakealarm_path ]];then

        echo "尝试wakealarm时钟方式测试" >> s3.log
        while [ $NUM -gt 0 ]
        do
        	cnum=`expr $1 - $NUM + 1`
        	echo "将进行  第 $cnum 次休眠" >> s3.log
        	sleep 3
        	echo "0" > /sys/class/rtc/rtc0/wakealarm
            echo "+60" > /sys/class/rtc/rtc0/wakealarm
            is_success "写入指定时间" >> s3.log
            systemctl suspend
            is_success "wakealarm时钟" >> s3.log
        	NUM=`expr $NUM - 1`
        done

    else
        echo "该机器不支持wakealarm时钟自动唤醒功能" >> s3.log
        
       $wakeonlan
       if [[ $wakeonlan =~ "not" ]];then
           echo "该机器不支持网络唤醒功能" >> s3.log
       else
           echo "该机器支持网络唤醒，需要在bios中设置开启网络唤醒，已经系统中设置网卡的网络唤醒启用：ethtool -s 网卡名 wol g"  >> s3.log
       fi
    fi
fi


