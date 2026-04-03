#!/bin/bash


if [ $('whoami') != 'root' ];then
    echo "请使用root用户执行！！!";
    sleep 1
    exit
fi

# 自启动变量
TESTPATH=/home/uos
run_path=/lib/systemd/system/autoTest.service
run_txt=$TESTPATH/logs/run.txt
run_log=$TESTPATH/logs/run.log
run_conf=$TESTPATH/logs/run.conf
install_txt=$TESTPATH/logs/install.txt


function open_test_conf(){
    # 运行配置
    cd $TESTPATH
    if [[ ! -d logs ]]; then
        system_type=$(grep "^NAME=" /etc/os-release |awk -F "=" '{print $2}'  | sed 's/\"//g')

        if [ "$system_type" = "Kylin" ];then
            apt update
            apt install xdotool
        fi
        
        mkdir logs
        echo "run-number 1" > $TESTPATH/logs/run.conf
        touch  $run_txt
        chmod 777 -R logs
    fi


    # 自启配置
    if [[ -x $run_path ]];then
        echo "存在自启动"
        # 重新加载配置文件
        systemctl daemon-reload
        systemctl enable autoTest.service
    else
        cat > $run_path << EOF
[Unit]
Description=test
After=network.target
After=lightdm.service
[Service]
Type=simple
ExecStart=/bin/bash /home/uos/autoTest.sh -r
User=uos
[Install]
WantedBy=multi-user.target
EOF
        chmod 777 $run_path
        # 重新加载配置文件
        systemctl daemon-reload
        systemctl enable autoTest.service
        echo "自启配置写入成功"
    fi


    # 设置自动登录并清空秘钥环
    function set_autoLogin(){
        dbus-send --system --dest=com.deepin.daemon.Accounts --print-reply /com/deepin/daemon/Accounts/User1000 com.deepin.daemon.Accounts.User.EnableNoPasswdLogin boolean:true
        dbus-send --system --dest=com.deepin.daemon.Accounts --print-reply /com/deepin/daemon/Accounts/User1000 com.deepin.daemon.Accounts.User.SetAutomaticLogin boolean:true
        rm -f /home/uos/.local/share/keyrings/*
    }
    set_autoLogin
}

open_test_conf

echo "配置完成，重启后开启测试"
sleep 10
reboot