#!/bin/bash


# 自启动变量
TESTPATH=/home/uos/
run_pwd=$TESTPATH/reboot.py
run_path=/etc/xdg/autostart/reboot_test.desktop

#自启服务
function reboot_server(){
    if [[ -f $run_path ]];then
        echo "自启已存在"
    else
        cat > $run_path << EOF
[Desktop Entry]
Name=portTest
Exec=/home/uos/systemMacroPerformanceAutoTest/autoTest.sh
Type=Application
EOF
    fi
}

function run_main(){
    #获取总次数
    totalTimes=$(cat $TESTPATH/count_reboot.info |awk 'NR==1{print $0}')

    #获取执行次数
    frequencyTimes=$(cat $TESTPATH/count_reboot.info |awk 'NR==2{print $0}')

    #计算剩余次数
    remainingTimes=$(( $totalTimes - $frequencyTimes ))



    if [ $remainingTimes > 1 ];then
        sleep 1

        # 开启自启服务
        reboot_server
        sleep 1

        # 获取的执行次数+1 写入配置文件
        count=$(( $frequencyTimes + 1 ))
        sleep 1
        # echo $frequencyTimes >> $TESTPATH/reboot.log
        sleep 1
        echo $count >> $TESTPATH/reboot.log
        sleep 1
        # echo -e "$totalTimes\n$count" > $TESTPATH/count_reboot.info

        time=$(date +%Y%m%d_%H-%M-%S)
        echo  "$time  第 $count 次重启" >>  $TESTPATH/reboot.log
        sleep 1
        cat  $TESTPATH/reboot.log
        sleep 1
        # 开始重启
        reboot
    else
        # 关闭自启服务
        systemctl disable rebootTest.service
        sleep 1
        # 删除自启文件
        rm  $run_path
        # 删除配置文件
        rm -rf $TESTPATH/count_reboot.info
        rm -rf $TESTPATH/wrietpath.sh
        echo "重启测试已经完成"
        systemctl enable test.service
        reboot
    fi
}      

run_main