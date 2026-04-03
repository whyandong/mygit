#!/bin/bash

#需要确保设备支持网络/rtc唤醒

if [ $# = 1 ];then
    for (( i=1; i<=$1; i++ ))
    do
        # 如果是飞腾设备需要blos 开启网络唤醒
        cpuinfo=$(lscpu |awk '/Vendor ID:/{print $NF}')
        if [ $cpuinfo == "Phytium" ]; then
            networkinfo=$(ip a | awk '/state UP/{print $2}'| awk -F ":" '{print $1}')
            echo 1 | sudo -S ethtool -s $networkinfo wol g
            MAC=$(ip a | grep -A 1 $networkinfo | awk '/ether/{print $(NF-2)}')
            sed_mac="{""\"""IP""\"":"\""$MAC"\"""}"
            curl -X POST -H 'Content-Type:application/json' -d $sed_mac "http://10.20.53.202:6666/wake"
        else
            rtcwake -s 60
        fi

        # 状态，进行不同种类的测试需要更换dbus的最后一个接口（Suspend 待机/Hibernate 休眠）
        dbus-send --session --dest=com.deepin.dde.shutdownFront --print-reply /com/deepin/dde/shutdownFront com.deepin.dde.shutdownFront.Hibernate
    done
else
    echo "bash net_work_wake_up.sh 次数"
fi