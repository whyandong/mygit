#!/bin/bash

#File    :   speccpu_run.sh
#Time    :   2021/10/14 14:32:00
#Author  :   xiongzhen
#Version :   1.0
#Contact :   xiongzhen@uniontech.com

echo "当前用户是："
whoami

if [ $('whoami') != 'root' ];then
  echo "请使用root用户执行！！!";
  sleep 1
  exit
fi


test_path=/home/speccpu
url_login="https://filewh.uniontech.com/accounts/login/"
#访问共享链接下载
url_3A5000="https://filewh.uniontech.com/f/9d033ec96cf742fd9887/?dl=1"
url_3A4000="https://filewh.uniontech.com/f/bc01ca679c904f3b8abc/?dl=1"
url_ft2000="https://filewh.uniontech.com/f/33773009cb124ff8bbaa/?dl=1"
url_hygon="https://filewh.uniontech.com/f/f3998cc2f6b247ebb169/?dl=1"
url_d2000="https://filewh.uniontech.com/f/b12804dc684b4ce7b616/?dl=1"
url_zhaoxin="https://filewh.uniontech.com/f/d4583fa05c814cc29b78/?dl=1"
url_3A3000="https://filewh.uniontech.com/f/2a60bef2265c4480b079/?dl=1"
url_intel="https://filewh.uniontech.com/f/750886bf2f7445919930/?dl=1"

#识别CPU型号，并输出
model_name=`lscpu|grep "Model name"|awk -F' ' '\
    {for(i=3;i<=NF;i++)\
        {if($i ~ /Intel/)\
            {print "intel";exit}\
        else if($i ~ /Loongson-3A5000/)\
            {print "3A5000";exit}\
        else if($i ~ /FT-2000/)\
            {print "FT";exit}\
        else if($i ~ /Hygon/)\
            {print "Hygon";exit}\
        else if($i ~ /D2000/)\
            {print "D2000";exit}\
        else if($i ~ /Loongson-3A4000/)\
            {print "3A4000";exit}\
        else if($i ~ /ZHAOXIN/)\
            {print "ZHAOXIN";exit}\
        else if($i ~ /Loongson-3A3000/)\
            {print "3A3000";exit}\
        else\
            {if (i==NF)\
                {print "未适配本机CPU型号"}\
            else\
                {continue}\
            }\
        }\
    }\
'`

#下载文件，如果不存在或者文件大小为0，则下载,
function download_file(){
    if [[ ! -s $1 ]]; then
        #判断seafile服务是否OK
        seafile_status=`wget --server-response --spider  --quiet $url_login 2>&1 |grep HTTP|awk '{print$2}'`
        if [[ $seafile_status != "200" ]]; then
            echo "seafile无法访问，请稍后再试！！！"
            exit 
        fi
        #获取登陆页面cookie
        curl -s -o /dev/null -c cookies_tmp1 $url_login
        cookie=`cat cookies_tmp1 |grep sfcsrftoken|awk '{print $7}'`
        #使用登陆页面cookie中的sfcsrftoken作为登陆参数之一，并保存登陆成功的cookie
        curl -b cookies_tmp1 -c cookies_tmp2 -d"csrfmiddlewaretoken=$cookie&login=xiongzhen@uniontech.com&password=qq941201@" $url_login
        sessionid=`cat cookies_tmp2 |grep sessionid|awk '{print $7}'`
        #使用登陆成功后的cookie的sessionid进行下载任务
        wget --header="cookie: sessionid=$sessionid" -O $1 $2
        #下载完后清理cookie文件
        rm -rf cookies_tmp* 
    fi
}

function install_speccpu(){
    if [[ ! -d $test_path ]];then
        mkdir -p $test_path
    fi
    cd $test_path
    if [[ ! -s speccpu.zip ]];then
        rm -rf speccpu.zip
        download_file speccpu.zip $1
        unzip speccpu.zip
        if [[ $? -ne 0 ]];then
            echo "请检查curl工具是否存在或下载url是否过期！"
            echo "请删除安装目录$test_path后再执行脚本"
            exit
        else
            echo "解压成功"
        fi
    fi
}

function install_ft(){
    if [[ ! -d /home/phytium ]];then
        mkdir -p /home/phytium
    fi
    cd /home/phytium
    if [[ ! -s speccpu.zip ]];then
        rm -rf speccpu.zip
        download_file speccpu.zip $1
        unzip speccpu.zip
        if [[ $? -ne 0 ]];then
            echo "请检查curl工具是否存在或下载url是否过期！"
            echo "请删除安装目录/home/phytium后再执行脚本"
            exit
        else
            echo "解压成功"
        fi
    fi
}

function run_3A4000(){
    install_speccpu $url_3A4000
    cd $test_path/speccpu2006
    if [[ ! -d spec-32lib ]];then
        tar -xzvf spec-32lib.tar.gz
        cp spec-32lib/* /lib
    fi
    if [[ ! -d cpu2006-v1.1 ]];then
        tar -xzvf cpu2006-v1.1-128.tar.gz
    fi
    cd cpu2006-v1.1
    bash build_and_run_128.sh
}

function run_3A5000(){
    install_speccpu $url_3A5000
    cd $test_path/cpu2006-v1.1
    bash myrun.sh
}

function run_3A3000(){
    install_speccpu $url_3A3000
    cd $test_path/spec2006-loongson
    bash myrun.sh
}

function run_intel(){
    install_speccpu $url_intel
    cd $test_path/cpu2006
    bash run
}

function run_d2000(){
    install_speccpu $url_d2000
    cd $test_path/speccpu/spec2006
    bash install.sh << EOF
    y
EOF
    source shrc
    bash run_test_new.sh << EOF
    1
    a
    3
EOF
}

function run_ft(){
    install_ft $url_ft2000
    cd /home/phytium/speccpu/spec2006
    bash install.sh << EOF
    y
EOF
    source shrc
    bash run_test.sh << EOF
    1
    a
    3
EOF
}

function run_hygon(){
    install_speccpu $url_hygon
    cd $test_path
    if [[ ! -d /home/spec2006 ]];then
        bash Hygon_speccpu.sh -b
    else
        bash Hygon_speccpu.sh -r
    fi
}

function run_zhaoxin(){
    install_speccpu $url_zhaoxin
    chmod -R a+x $test_path/speccpu2006-v1.0.1
    cd $test_path/speccpu2006-v1.0.1
    . ./shrc
    runspec -V
    if [[ $? -ne 0 ]];then
        apt update
        if [ $? != 0 ];then
            echo "确定网络和源码正常可用"
            exit
        else
            apt install -y gcc g++ gfortranli bbz2-dev
        fi
        if [[ ! -a /usr/lib/x86_64-linux-gnu/libbz2.so.0 ]];then
            cp /usr/lib/x86_64-linux-gnu/libbz2.so /usr/lib/x86_64-linux-gnu/libbz2.so.0
        fi
        bash install.sh << EOF
        y
EOF
        . ./shrc
        cp config/x86.cfg config/default.cfg
        runspec –c x86.cfg -n 1 all
    else
        runspec –c x86.cfg -n 1 all
    fi
}

case $model_name in
    3A5000)
        run_3A5000
        ;;
    3A4000)
        run_3A4000
        ;;
    3A3000)
        run_3A3000
        ;;    
    Hygon)
        run_hygon
        ;;
    FT)
        run_ft
        ;;
    D2000)
        run_d2000
        ;;
    ZHAOXIN)
        run_zhaoxin
        ;;
    intel)
        run_intel
        ;;
    *)
        echo $model_name
        exit 1
        ;;
esac