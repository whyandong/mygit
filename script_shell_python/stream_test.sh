#!/bin/bash
TESTPATH=/home/uos

read -p "请输入物理核数：（如：1）" cpus
read -p "请输入CPU最大缓存，单位为MB：（如：2）" cachem

function install_stream(){
    cd $TESTPATH/package
    # download_file stream.zip $stream_path
    #已存在，则删除
    if [[ -d "Stream" ]]; then
        rm -rf Stream
    fi
    #apt install -y make g++ gfortran
    unzip Stream.zip
    # cd Stream
    # # make
}



#测试stream
#测试3次，每次测试前清空缓存
function stream_test(){

    cd $TESTPATH/package/Stream

    #根据公式计算出DSTREAM_ARRAY_SIZE的值
    size=`echo "$cachem * $cpus * 4.1 * 1024 * 1024"|bc`
    size1=`echo "$size/8"|bc`

    sed -i "58s/2000000/$size1/" stream.c

    for (( i=1;i<4;i++ ))
    do
    #单线程
        gcc -O3 -DNTIMES=30  stream.c -o stream
        ./stream >> $TESTPATH/logs/stream_单线程.txt
        echo "结果成功写入单线程.txt"

        #满线程
        gcc -O3 -fopenmp -DNTIMES=30  stream.c -o stream
        ./stream >> $TESTPATH/logs/stream_满线程.txt
        echo "结果成功写入满线程.txt"
    done
    echo "stream 3次测试完成，测试结果见logs目录"
}

install_stream
stream_test