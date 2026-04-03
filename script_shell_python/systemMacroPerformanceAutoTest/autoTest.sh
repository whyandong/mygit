#!/bin/bash


cat  << EOF

/home/uos下运行测试脚本，bash autoTest.sh -s system_type
-s 环境部署
system_type 系统类型(uos/kylin)

用户名必须为:<uos>，密码:<1>
飞腾设备将使用网络唤醒
请保证内网连接正常，EAP认证如果连接名为网卡，需要手动删除网卡名的连接，新建有线连接进行EAP认证
麒麟需要关闭 <应用控制与保护>设置，<账户安全>密码强度关闭全部设置，长度为1，种类为1，更改密码为<1>

不支持的设备：
        宝德鲲鹏（不支持，网络/rtc唤醒）,测试时需要手动唤醒
        攀升(S3流程实际是S2)，获取不到S3相关日志
EOF

sleep 23

# 系统判断
system_type=$(grep "^NAME=" /etc/os-release |awk -F "=" '{print $2}'  | sed 's/\"//g')


function eject_window (){
    export DISPLAY=:0

    if [ "$system_type" = "Kylin" ];then
        xdotool mousemove 964 482 click 2
        sleep 1
        xdotool mousemove 1023 759 click 1
        sleep 1
    else
        xdotool key alt+ctrl+t
    fi
    

    # dbus-send --session --print-reply --dest=com.deepin.SessionManager /com/deepin/StartManager com.deepin.StartManager.Launch string:/usr/share/applications/deepin-terminal.desktop

    sleep 2

    xdotool type --delay 100 'cd /home/uos/'

    xdotool key Return



}


# 自启动变量
TESTPATH=/home/uos
run_path=/lib/systemd/system/autoTest.service
run_txt=$TESTPATH/logs/run.txt
run_log=$TESTPATH/logs/run.log
run_conf=$TESTPATH/logs/run.conf
install_txt=$TESTPATH/logs/install.txt

while getopts ":s:r:" opt
do
    case $1 in
        -s|--setup)
            eject_window
            
            xdotool type --delay 100 'sudo su'
            xdotool key Return

            xdotool type '1'
            xdotool key Return

            xdotool type --delay 100 'bash testConf.sh'
            xdotool key Return

            ;;
        -r|--restart)
            eject_window
            xdotool type --delay 100 'bash testItem.sh'
            xdotool key Return
            
            ;;
        ?)
            echo -e "bash autoTest.sh -s 第一次运行，环境部署，开始测试"
            echo -e "bash autoTest.sh -r 自启默认参数-r"
            
            echo -e "必须设置 用户名 uos，密码 1"
            echo -e "麒麟需要开启自动登录，关闭锁屏，麒麟无法连接内网服务器，不能使用网络唤醒需要进行手动唤醒"

            ;;
    esac
done