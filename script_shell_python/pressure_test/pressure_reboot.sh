#!/bin/bash



echo "当前用户是："
whoami

if [ $('whoami') != 'root' ];then
  echo "请使用root用户执行！！!";
  sleep 1
  exit
fi


# 获取平台类型，1为服务器版本，0为桌面版本
PlatForm=`uname -r |grep server|wc -l`
# 获取环境CPU 核数
CPU_N=`cat /proc/cpuinfo |grep processor|wc -l|tr -d "\n"`

#获取CPU架构
SYSARCH=`uname -m`
#获取内存大小
mem_size=`awk '($1=="MemTotal:"){printf  "%0.0f",$2/1024/1024}' /proc/meminfo`

#更正内存大小
function resize_mem(){
    size=1
    while [[ $1 -ge $size ]]; do
        size=`expr $size \* 2`
        if [[ $1 -eq $size ]]; then
            break
        fi
    done
    return $size
}

resize_mem $mem_size

MEM=$?
MEM2=`expr $MEM \* 2`
MEM_2=`expr $MEM / 2`



# 自启动变量
TESTPATH=/home/uos/pressure_test
run_pwd=$TESTPATH/run.sh
run_path=/lib/systemd/system/test.service
run_txt=$TESTPATH/logs/run.txt
run_log=$TESTPATH/logs/run.log
run_conf=$TESTPATH/logs/run.conf
install_txt=$TESTPATH/logs/install.txt

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




#设置自动登录并清空秘钥环
function set_autoLogin(){
    dbus-send --system --dest=com.deepin.daemon.Accounts --print-reply /com/deepin/daemon/Accounts/User1000 com.deepin.daemon.Accounts.User.EnableNoPasswdLogin boolean:true
    sleep 1
    dbus-send --system --dest=com.deepin.daemon.Accounts --print-reply /com/deepin/daemon/Accounts/User1000 com.deepin.daemon.Accounts.User.SetAutomaticLogin boolean:true
    sleep 1
    rm -f /home/uos/.local/share/keyrings/*
    sleep 1
}

#关闭自动登录
function off_autoLogin(){
    dbus-send --system --dest=com.deepin.daemon.Accounts --print-reply /com/deepin/daemon/Accounts/User1000 com.deepin.daemon.Accounts.User.EnableNoPasswdLogin boolean:false
    sleep 1
    dbus-send --system --dest=com.deepin.daemon.Accounts --print-reply /com/deepin/daemon/Accounts/User1000 com.deepin.daemon.Accounts.User.SetAutomaticLogin boolean:false
    sleep 1
}


#安装glxgears
function install_glxgears(){
    apt install -y mesa-utils
    is_success "安装glxgears"
}

#测试glxgears
function glxgears_test(){
    export  vblank_mode=0 && glxgears >> $TESTPATH/logs/glxgears.log &
    sleep 259200
    echo `ps -ef | grep glxgears | grep -v grep | awk '{print $2}' | xargs kill`
    sleep 3
    sed -i '1d;$d' $TESTPATH/logs/glxgears.log
}

# 安装x11perf
function install_x11perf(){
    apt install x11-apps -y
    is_success "安装x11perf"
}



#安装glmark
function install_glmark(){
    cd $TESTPATH/src
    # download_file glmark2.zip $glmark_path
    apt install -y git g++ build-essential pkg-config  libx11-dev libjpeg-dev  libpng-dev
    apt install -y libgl1-mesa-dev libpng12-dev libudev-dev libgles2-mesa-dev libgbm-dev
    #已存在，则删除
    if [[ -d "glmark2" ]]; then
        rm -rf glmark2
    fi
    unzip glmark2.zip
    cd glmark2/
    #针对麒麟镜像修改编码格式
    sed -i '3a import sys\nreload(sys)\nsys.setdefaultencoding("utf-8")' waflib/Logs.py 
    ./waf configure --with-flavors=x11-gl
    is_success
    ./waf build -j4
    is_success "编译glmark"
    ./waf install
    is_success
    strip -s /usr/local/bin/glmark2
    is_success "安装glmark"
}


#测试glmark
function glmark2_test(){
    cd $TESTPATH
    glmark2 --run-forever
}

# 图形测试
function graphic_stability_test(){
    
    glmark2_test &
    sleep 1
    glxgears_test &
    sleep 1
    x11perf -all -repeat 259200 &
    sleep 259200
}


#测试s3
function s3_test(){
    cd $TESTPATH/src
    bash S3_100.sh
}

function install_clone(){
    cd $TESTPATH/src
    apt install git -y
    if [ ! -d "/home/uos/pressure_test/src/ltp" ];then
        count=1
        while [ 1 ]
        do
            echo $(date +%Y-%m-%d_%H:%M:%S) "第" $count "次克隆ltp工程"
            git clone https://github.com/linux-test-project/ltp.git
            sleep 1
            if [ -d "/home/uos/pressure_test/src/ltp" ];then
                break
            else
                echo $(date +%Y-%m-%d_%H:%M:%S) "第" $count "次克隆ltp失败，准备重试"
                count=$(($count+1))
                continue
            fi
        done
    fi
}

#测试s4
function s4_test(){
    cd $TESTPATH/src
    bash S4_100.sh
}

# 测试重启
function reboot_test(){
    cd $TESTPATH/src
    python3 reboot.py 501

}

# 测试ltp功能
function ltp_functional_test(){
    cd $TESTPATH/src
    python3 ltp.py -f
}

# ltp压力测试
function ltp_pressure_test(){
    cd $TESTPATH/src
    systemctl disable test.service
    python3 ltp.py -p 24
}

# 静止测试
function static_test(){
    dbus-send --session --print-reply --dest=org.freedesktop.FileManager1 /com/deepin/filemanager/filedialog/9184f2bdfa5542a487b1cf036555c104 com.deepin.filemanager.filedialog.show
    
    sleep 8640
}


#安装完第一重启
function first_reboot(){
    echo first_reboot >> $run_txt
    sleep 3
    reboot
}



#桌面性能测试
function desktop_test(){
	if [ $run_number == 1 ];then
		install_list=(install_glmark install_glxgears install_x11perf install_clone)
		run_list=(first_reboot graphic_stability_test s3_test s4_test reboot_test staticTest ltp_functional_test ltp_pressure_test)
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

    # 执行测试
    for run_i in ${run_list[*]};do
        echo "已完成以下测试："
        cat $run_txt |grep $run_i
        if [[ $? -ne 0 ]];then
            echo "5分钟之后开始$run_i测试，请等待......."
            sleep 180
            echo "$run_i测试中....."
            echo "$run_i未测试,进行测试"  >> $run_log
            echo "---------------开始$run_i测试，开始时间:---------------" >> $run_log
            echo `date` >> $run_log
            sync&&echo 3  > /proc/sys/vm/drop_caches
            $run_i 2>> $run_log
            echo "---------------结束$run_i测试，结束时间:---------------" >> $run_log
            echo `date` >> $run_log
            echo $run_i >> $run_txt
            echo "$run_i测试完成"
            systemd-analyze >> $TESTPATH/logs/bootTime.log
            echo "即将进行重启，测试下一项"
            sleep 10
            reboot
        else
            echo "$run_i测试，跳过，进行下一项"  >> $run_log
            continue
        fi
    done
    
    echo "全部测试完成"  >> $run_log
    off_autoLogin
    is_success "关闭自动登录"
    systemctl disable test.service
    rm -rf $run_path

    lscpu > $TESTPATH/logs/cpuname.conf
    echo "================================= 测试已经完成 ========================================="
}



# 主程序
function main_test(){
    #is_success "apt更新"
    cd $TESTPATH
    if [[ ! -d logs ]]; then
        mkdir logs
    fi

    if [[ -x $run_path ]];then
        echo "存在自启动"
        # 重新加载配置文件
        systemctl daemon-reload
        systemctl enable test.service
    else
        cat > $run_path << EOF
[Unit]
Description=test
After=network.target
After=lightdm.service
[Service]
Type=simple
ExecStart=/usr/bin/bash $run_pwd
User=uos
[Install]
WantedBy=multi-user.target
EOF
        chmod 777 $run_path
        # 重新加载配置文件
        systemctl daemon-reload
        systemctl enable test.service
        rm -rf $run_txt
        rm -rf $run_log
        rm -rf $run_conf
        echo "设置自启动成功"
        #is_success "关闭窗口特效和设置电源管理"
        set_autoLogin
        is_success "设置自动登录"
        sleep 3

        echo run-number 1 >> $run_conf 
        sleep 5
        reboot
    fi
    #判断是否为桌面版
    if [[ $PlatForm -eq 0 ]]; then
        desktop_test
    fi
}

main_test
