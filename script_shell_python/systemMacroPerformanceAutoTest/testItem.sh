#!/bin/bash



# 电源管理设置（待机，锁定，休眠,唤醒锁屏）
function off_acpi_manager(){
        # 设置待机时间为从不
        dbus-send --session --dest=com.deepin.daemon.Power --print-reply /com/deepin/daemon/Power org.freedesktop.DBus.Properties.Set string:com.deepin.daemon.Power string:LinePowerSleepDelay variant:int32:0

        # 设置锁定时间为从不
        dbus-send --session --dest=com.deepin.daemon.Power --print-reply /com/deepin/daemon/Power org.freedesktop.DBus.Properties.Set string:com.deepin.daemon.Power string:LinePowerLockDelay variant:int32:0

        # 设置锁定时间为从不
        dbus-send --session --dest=com.deepin.daemon.Power --print-reply /com/deepin/daemon/Power org.freedesktop.DBus.Properties.Set string:com.deepin.daemon.Power string:LinePowerScreenBlackDelay variant:int32:0

        # 关闭待机唤醒时需要密码
        dbus-send --session --print-reply --dest=com.deepin.daemon.Power /com/deepin/daemon/Power org.freedesktop.DBus.Properties.Set string:com.deepin.daemon.Power string:SleepLock variant:boolean:false

        # 关闭休眠唤醒时需要密码
        dbus-send --session --print-reply --dest=com.deepin.daemon.Power /com/deepin/daemon/Power org.freedesktop.DBus.Properties.Set string:com.deepin.daemon.Power string:ScreenBlackLock variant:boolean:false

        echo 1 > /home/uos/set.txt
    }

if [ ! -f "/home/uos/set.txt" ];then
    off_acpi_manager
fi


# 自启动变量
TESTPATH=/home/uos
run_path=/lib/systemd/system/autoTest.service
run_txt=$TESTPATH/logs/run.txt
run_log=$TESTPATH/logs/run.log
run_conf=$TESTPATH/logs/run.conf
install_txt=$TESTPATH/logs/install.txt

# 系统判断
system_type=$(grep "^NAME=" /etc/os-release |awk -F "=" '{print $2}'  | sed 's/\"//g')

#获取运行配置
run_number=0
if [ -s $run_conf ];then
    run_number=`awk '/run-number/{print $2}' $run_conf`
fi


#判断命令是否执行成功
function is_success(){
    if [[ $? -ne 0 ]]; then
        echo "$1失败"
        exit
    else
        echo "$1成功"
    fi
}

# 麒麟使用xdotool 完成用户页面模拟

function mouse_click(){
    xdotool mousemove 33 1060 click 1
    sleep 1
    xdotool mousemove 349 1006 click 1
    sleep 1
}


# 关机测试
function powerOff_test(){
    if [ "$system_type" = "Kylin" ];then
        mouse_click
    else
        dbus-send --session --dest=com.deepin.dde.shutdownFront --print-reply /com/deepin/dde/shutdownFront com.deepin.dde.shutdownFront.Shutdown
    fi
    sleep 5
    echo $run_i >> $run_txt
    echo "power_off_start_time: "$(date +%Y-%m-%d_%H:%M:%S) >> $TESTPATH/logs/timeRecordSheet.log


    if [ "$system_type" = "Kylin" ];then
        xdotool mousemove 1437 528; xdotool click 1
    else
        xdotool mousemove 929 613; xdotool click 1
    fi
    
}


# 开机测试
function powerOn_test(){

    sleep 5
    # 开机的日志开始时间
    time=$(echo 1 | sudo -S journalctl -b |awk '/running in system mode/{print $1,$2,$3}')
    echo "power_On_start_time: $time" >> $TESTPATH/logs/timeRecordSheet.log
    echo $run_i >> $run_txt

    # 开机到用户自动登录的时间
    time1=$(systemctl status session-* |awk '/active/{print $6,$7}')
    echo "power_On_end_time: $time1" >> $TESTPATH/logs/timeRecordSheet.log
}


# 重启测试
function reboot_test(){
    if [ "$system_type" = "Kylin" ];then
        mouse_click
    else
        dbus-send --session --dest=com.deepin.dde.shutdownFront --print-reply /com/deepin/dde/shutdownFront com.deepin.dde.shutdownFront.Restart
    fi
    sleep 5
    
    echo $run_i >> $run_txt
    echo "reboot_start_time: "$(date +%Y-%m-%d_%H:%M:%S) >> $TESTPATH/logs/timeRecordSheet.log
    
    if [ "$system_type" = "Kylin" ];then
        xdotool mousemove 1282 528; xdotool click 1
    else
        xdotool mousemove 929 613; xdotool click 1
    fi
    
}


# 待机测试
function standby_test(){
    
    echo "待机测试开始"
    stadby_x=100

    echo "待机变量：$stadby_x"
    if [ $stadby_x = 100 ];then
        echo $run_i >> $run_txt

        if [ "$system_type" = "Kylin" ];then
            mouse_click
        fi

        echo 1 | sudo -S dmesg | tail -1
        echo 1 | sudo -S dmesg | tail -1 > dmesg1
        stadby_time=$(echo 1 | sudo -S dmesg | tail -1 | cut -c 2-13)
        echo "standby_start_time: $stadby_time" >> $TESTPATH/logs/timeRecordSheet.log

        if [ "$system_type" = "Kylin" ];then
            xdotool mousemove 800 528; xdotool click 1
        else
            dbus-send --session --dest=com.deepin.dde.shutdownFront --print-reply /com/deepin/dde/shutdownFront com.deepin.dde.shutdownFront.Suspend
        fi
        
        stadby_x=`expr $stadby_x + 1`
    fi

    
    sleep 10
    echo "唤醒流程，准备记录时间"
    # 待机开始待机完成时间
    echo 1 | sudo -S dmesg |grep 'suspend entry'
    echo 1 | sudo -S dmesg | tail -1 > dmesg2
    time=$(echo 1 | sudo -S dmesg |grep 'suspend entry'| cut -c 2-13)
    echo "standby_lower_time: $time"  >> $TESTPATH/logs/timeRecordSheet.log

    # 待机被唤醒的开始时间
    echo 1 | sudo -S dmesg |grep 'CPU1 is up'
    time1=$(echo 1 | sudo -S dmesg |grep 'CPU1 is up'| cut -c 2-13)
    echo "standby_waken_start_time: $time1"  >> $TESTPATH/logs/timeRecordSheet.log

    # 待机被唤醒的结束时间
    echo 1 | sudo -S dmesg |grep 'suspend exit'
    time2=$(echo 1 | sudo -S dmesg |grep 'suspend exit'| cut -c 2-13)
    echo "standby_waken_end_time: $time2"  >> $TESTPATH/logs/timeRecordSheet.log
    echo "待机唤醒已经完成，准备重启" 
}


# 休眠测试
function dormancy_test(){

    echo "休眠测试开始"
    dormancy_x=100
    echo "休眠变量：$dormancy_x"

    if [ $dormancy_x = 100 ];then
        echo $run_i >> $run_txt

        echo 1 | sudo -S dmesg | tail -1
        dormancy_time=$(echo 1 | sudo -S dmesg | tail -1 | cut -c 2-13)
        echo "dormancy_start_time: $dormancy_time" >> $TESTPATH/logs/timeRecordSheet.log
        echo 1 |sudo -S su -c "echo reboot > /sys/power/disk && echo disk > /sys/power/state"
        dormancy_x=`expr $dormancy_x + 1`
    fi

    sleep 10
    echo "休眠唤醒流程，准备记录时间" 

    # 休眠唤醒后记录休眠的退出时间
    echo 1 | sudo -S dmesg |grep  'hibernation exit'
    time=$(echo 1 | sudo -S dmesg |grep  'hibernation exit'| cut -c 2-13)
    echo "dormancy_end_time: $time"   >> $TESTPATH/logs/timeRecordSheet.log
    echo "休眠唤醒已经完成，准备重启" 
}


# 测试开始
function desktop_test(){
    if [ $run_number == 1 ];then
        install_list=()
        run_list=(powerOff_test powerOn_test reboot_test standby_test dormancy_test)
    fi

    # 安装
    for l in ${install_list[*]};do
        cat $install_txt |grep $l 
        if [[ $? -ne 0 ]];then
            sleep 1
            $l
            echo $l >> $install_txt
            sleep 1
        else
            echo "$l 安装"
            continue
        fi
    done


    x=1
    # 执行测试
    for run_i in ${run_list[*]};do
        
        # 判断体内的代码只在首次进入循时执行
        if [ $x -eq 1 ];then
            test_option=$(awk 'END{print $1}' $run_txt)
            echo $test_option
            sleep 5
            if [ "$test_option" = "powerOff_test" ]; then
                echo "上次为关机流程，截取上一次用户日志的最后时间"
                sleep 5
                # 关机结束的最后一条日志时间
                echo 1| sudo -S journalctl -b -1 |awk 'END{print $1,$2,$3}'
                time5=$(echo 1| sudo -S journalctl -b -1 |awk 'END{print $1,$2,$3}')
                echo $time5
                sleep 5
                echo "power_off_end_time: $time5" >> $TESTPATH/logs/timeRecordSheet.log

            elif [ "$test_option" = "reboot_test" ]; then
                echo "上次为重启流程，截取本次用户的登录时间"
                sleep 5
                # 重启后用户自动登录的时间
                time6=$(systemctl status session-* |awk '/active/{print $6,$7}')
                echo "reboot_end_time: $time6" >> $TESTPATH/logs/timeRecordSheet.log
            fi
            x=`expr $x + 1`
        fi
        echo "已完成以下测试："
        
        cat $run_txt | grep $run_i

        if [[ $? -ne 0 ]]; then
            echo "即将开始$run_i测试，请等待......."
            sleep 5

            # 非重启测试需要使用唤醒功能，飞腾使用网络唤醒，其他使用rtc唤醒，鲲鹏不支持网络和rtc唤醒
            if [ "$run_i" != "reboot_test" ]; then
                # 如果是飞腾设备需要blos 开启网络唤醒
                cpuinfo=$(lscpu |awk '/Vendor ID:/{print $NF}')
                if [ "$cpuinfo" = "Phytium" ]; then
                    networkinfo=$(ip a | awk '/state UP/{print $2}'| awk -F ":" '{print $1}')
                    echo 1 | sudo -S ethtool -s $networkinfo wol g
                    MAC=$(ip a | grep -A 1 $networkinfo | awk '/ether/{print $(NF-2)}')
                    sed_mac="{""\"""IP""\"":"\""$MAC"\"""}"
                    curl -X POST -H 'Content-Type:application/json' -d $sed_mac "http://10.20.53.202:6666/wake"
                    echo "使用【网络】唤醒系统"
                else
                    echo 1 | sudo -S rtcwake -s 30
                    echo "使用【rtc】唤醒系统"
                fi
            fi

            $run_i 2 >> $run_log
            echo "$run_i----> 测试完成准备重启"
            sleep 5
            reboot
        else
            echo "$run_i测试，跳过，进行下一项"  >> $run_log
            continue
        fi
    done
    
    echo "全部测试完成"  >> $run_log
    echo 1 | sudo -S rm -rf $run_path

    lscpu > $TESTPATH/logs/cpuname.conf
    echo "================================= 测试已经完成 ========================================="
}


desktop_test