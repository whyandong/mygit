#! /bin/bash
#获取当前系统分区目录名
a=`blkid | awk '{print $1}' | sed -r 's/(.*):.*/\1/'`
echo $a
#遍历查询所有分区是否开启ACL权限
for data in ${a[@]}
do
	#echo ${data}
	dumpe2fs -h ${data} | grep "Default mount options"
done

