#!/bin/bash
touch type.txt
pwd=$(pwd)
mount=$(mount)
if [ `whoami` = "root" ];then
    read -p "请输入你的U盘分区名称（如U盘分区为/dev/sdb1,那么请输入sdb1就行）：" partname
    umount /dev/$partname
    fileFun(){
        touch test.txt
        mv test.txt test1.txt
        cp $pwd/type.txt /mnt
        rm -f test1.txt
        dd if=/dev/zero of=test.img bs=1M count=1024 oflag=direct
        file1="/mnt/type.txt"
        file2="/mnt/test.img"
        if [ ! -e $file1 ];then
            echo "文件操作出错"
            exit 0
        fi
        if [ ! -e $file2 ];then
            echo "磁盘读写出错"
            exit 0
        fi
        }
    pulicFun(){
        mount /dev/$partname /mnt
        if [[ $mount =~ $partname ]]
        then
            echo ${i}'结果是：'$(df -hT | grep $partname |awk '{print $2}') >> $pwd/type.txt 
            cd /mnt
            fileFun
            cd ..
            umount /dev/$partname
        else
            echo "没有成功挂载到mnt,请重新再执行脚本！"
            exit
        fi
        } 
    type1=(ext3 ext4 ntfs vfat xfs btrfs jfs reiserfs nilfs2 )
    
    for i in ${type1[@]}
    do
        if [[ $i == xfs || $i == btrfs ]]
        then
            echo $i
            echo y | mkfs.$i -f /dev/$partname
            pulicFun

        else
            echo y | mkfs.$i  /dev/$partname
            pulicFun
        fi   
    
    done
else
	echo "请登录root用户执行此脚本"
    exit
fi
