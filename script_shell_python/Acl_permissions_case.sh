#! /bin/bash
DATE=$(date +"%Y-%m-%d %H:%M:%S")
#遍历目录校验递归权限
prove(){
	can=$1
	c=(test01 test01/test02 test01/test02/case1.sh test01/test02/case2.sh)
	for data in ${c[@]}
	do
	#echo $can
	a=`getfacl ${data} | awk '{print $1}' | grep wang | sed -r 's/user:wang:(.*).*/\1/' `
	#echo $?
	#if [ $a == 'r--' ]; then	
	if [ "$a" == "$can" ]; then
	echo "测试ACL权限路径：$data 测试时间：$DATE  测试结果：Pass"
	else
 		 echo "测试ACL权限路径：$data 测试时间：$DATE 测试结果： Fail" 
	fi	
	done
}
#验证文件目录权限方法
prove1(){
	can=$1
	c=(test01 test01/test02)
	for data in ${c[@]}
	do
	a=`getfacl ${data} | awk '{print $1}' | grep default:user:wang | sed -r 's/default:user:wang:(.*).*/\1/' `	      #echo $?
	#echo $can
	#echo $a
	if [ "$a" == "$can" ]; then
	echo "测试ACL权限路径：$data 测试时间：$DATE  测试结果：Pass"
	else
 		 echo "测试ACL权限路径：$data 测试时间：$DATE 测试结果： Fail" 
	fi	
	done
}
#验证默认递归后创建文件继承权限方法
prove2(){
	can=$1
	c3=(test01/test02/case3.sh)
	for data in ${c3[@]}
	do
	a=`getfacl ${data} | awk '{print $1}' | grep wang | sed -r 's/user:wang:(.*).*/\1/' `	
	#echo $?
	if [ "$a" == "$can" ]; then
	echo "测试ACL权限路径：$data 测试时间：$DATE  测试结果：Pass"
	else
 		 echo "测试ACL权限路径：$data 测试时间：$DATE 测试结果： Fail" 
	fi	
	done
}
#验证创建文件默认最大权限方法
prove3(){
	
	a=`getfacl $c3 | awk '{print $1}' | grep mask | sed -r 's/mask::(.*).*/\1/' `	
	#echo $?
	if [ "$a" == "rw-" ]; then
	echo "测试ACL权限路径：$c3 测试时间：$DATE  测试结果：Pass"
	else
 		 echo "测试ACL权限路径：$c3 测试时间：$DATE 测试结果： Fail" 
	fi	
}
#验证清除用户权限方法
prove4(){
	c=(test01 test01/test02/case1.sh)
	for data in ${c[@]}
	do
	a=`getfacl ${data} | awk '{print $1}' | grep wang | sed -r 's/user:wang:(.*).*/\1/' `
	b=`echo $?`
	echo $a
	echo $b
	if [ ! -n "$a" ]; then
		echo "测试ACL权限路径：$c 测试时间：$DATE  测试结果：Pass" 
	else
		 echo "测试ACL权限路径：$c 测试时间：$DATE 测试结果： Fail" 
	fi
	done	
}


#验证清除所属组权限方法
prove5(){
	c=(test01 test01/test02/case1.sh)
	for data in ${c[@]}
	do
	a=`getfacl ${data} | awk '{print $1}' | grep wang2 | sed -r 's/group:wang2:(.*).*/\1/' `
	echo $a
	if [ ! -n "$a" ]; then
		echo "测试ACL权限路径：$c 测试时间：$DATE  测试结果：Pass"
	else
		 echo "测试ACL权限路径：$c 测试时间：$DATE 测试结果： Fail" 
	fi
	done	
}
#递归赋权方法
empower_recs(){
	basepath=$(cd `dirname $0`; pwd)
	path=$basepath/test01/
	can1=$1
	setfacl -R -m u:wang:$can1 $path
	#echo $?
}
#默认递归赋权方法
empower_default(){
	basepath=$(cd `dirname $0`; pwd)
	path=$basepath/test01/
	can1=$1
	setfacl -R -m d:u:wang:$can1 $path
	#echo $?
}
#赋权组方法
empower_group(){
	basepath=$(cd `dirname $0`; pwd)
	path=$basepath/test01/
	can1=$1
	setfacl -m g:wang2:$can1 $path
	#echo $?
}
#清除ACL权限方法
clear_all_acl(){
	path=$1
	setfacl -b  $path/		
	echo $?
}
#清除指定用户ACK权限方法
clear_user_acl(){
	user1=$1
	file=$2
	setfacl -x $user1 $file
	#echo $?
}
#清除指定所属组ACK权限方法
clear_group_acl(){
	group=$1
	file=$2
	setfacl -x g:$group $file
}
#创建基础文件/目录数据
baseData(){
	basepath=$(cd `dirname $0`; pwd)
	path=$basepath/test01
	filepath=$path/test02
	USER_COUNT=`cat /etc/passwd | grep '^zheng:' -c`
	USER_NAME='zheng'
	if [ $USER_COUNT -ne 1 ]
	then
		useradd -m $USER_NAME
		echo "$USER_NAME:123456" | chpasswd
		echo "用户不存在，开始创建用户"
	else
		echo "user $USER_NMAE existing"
	fi
	USER_COUNT1=`cat /etc/passwd | grep '^wang:' -c`
	USER_NAME1='wang'
	if [ $USER_COUNT1 -ne 1 ]
	then
		useradd -m $USER_NAME1
		echo "$USER_NAME1:123456" | chpasswd
		echo "用户不存在，开始创建用户"
	else
		echo "user $USER_NMAE1 existing"
	fi
	groupadd wang1
	groupadd wang2
	mkdir -p $filepath
	touch $filepath/case1.sh
	touch $filepath/case2.sh
	#echo " echo '1' " >  $filepath/case1.sh
	#echo " echo '1' " >  $filepath/case2.sh
	chmod -R 770 $path/
	chown -R zheng:wang1 $path/
	}	

basepath=$(cd `dirname $0`; pwd)
file_name=$basepath/test01/
echo "请将脚本放到已经开启ACL权限的逻辑分区目录下执行，实现对该目录的ACL权限校验，如：/目录，/data目录，/boot目录"
echo "脚本5秒后开始执行"
#sleep 5
 if [ ! -d "$file_name" ] ; then
	echo "基础数据不存在，开始创建基础测试环境"
 	baseData
else	
	echo "$file_name 目录已存在，请检查是否已运行过测试脚本，如需要重新运行，请先删除/变更 $file_name 目录"
	exit 2
 fi
<<dang1
#验证递归权限分配
case1="-w-"
clear_all_acl $file_name
echo "case1 :执行递归赋权，校验用户wang 的 -w- ACL 权限"
empower_recs $case1
prove $case1

case2="r--"
clear_all_acl $file_name
echo "case2 :执行递归赋权，校验用户wang 的 r-- ACL 权限"
empower_recs $case2
prove $case2

case3="--x"
clear_all_acl $file_name
echo "case3 :执行递归赋权，校验用户wang 的 --x ACL 权限"
empower_recs $case3
prove $case3

case4="rw-"
clear_all_acl $file_name
echo "case4 :执行递归赋权，校验用户wang 的 rw- ACL 权限"
empower_recs $case4
prove $case4

case5="-wx"
clear_all_acl $file_name
echo "case5 :执行递归赋权，校验用户wang 的 -wx ACL 权限"
empower_recs $case5
prove $case5

case6="r-x"
clear_all_acl $file_name
echo "case6 :执行递归赋权，校验用户wang 的 r-x ACL 权限"
empower_recs $case6
prove $case6

case7="---"
clear_all_acl $file_name
echo "case7 :执行递归赋权，校验用户wang 的 --- ACL 权限"
empower_recs $case7
prove $case7
#dang
#验证默认权限分配
case8="-w-"
clear_all_acl $file_name
echo "case8 :执行默认递归赋权，校验用户wang 的 -w- ACL 权限"
empower_default $case8
prove1 $case8

case9="r--"
clear_all_acl $file_name
echo "case9 :执行默认递归赋权，校验用户wang 的 r-- ACL 权限"
empower_default $case9
prove1 $case9

case10="--x"
clear_all_acl $file_name
echo "case10 :执行默认递归赋权，校验用户wang 的 --x ACL 权限"
empower_default $case10
prove1 $case10

case11="rw-"
clear_all_acl $file_name
echo "case11 :执行默认递归赋权，校验用户wang 的 rw- ACL 权限"
empower_default $case11
prove1 $case11

case12="-wx"
clear_all_acl $file_name
echo "case12 :执行默认递归赋权，校验用户wang 的 -wx ACL 权限"
empower_default $case12
prove1 $case12

case13="r-x"
clear_all_acl $file_name
echo "case13 :执行默认递归赋权，校验用户wang 的 r-x ACL 权限"
empower_default $case13
prove1 $case13

case14="---" 
clear_all_acl $file_name
echo "case14 :执行默认递归赋权，校验用户wang 的 --- ACL 权限"
empower_default $case14
prove1 $case14
#<<dang1
#默认赋权后 创建文件权限仅满足rw
case15="rw-"
clear_all_acl $file_name
echo "case 15默认递归赋予wang $case15 ACL权限，验证创建的文件继承默认权限"
empower_default $case15
touch $file_name/test02/case3.sh
prove2 $case15
#创建的文件 ACL mask最大权限默认仅支持rx
echo "case16 默认递归赋予wang $case15 ACL权限 ，创建的文件，acl默认不宜存在rwx权限，仅存在rw权限"
prove3

case17="r--"
rm -rf $file_name/test02/case3.sh
clear_all_acl $file_name
echo "case17默认递归赋予wang $case17 ACL权限，验证创建的文件继承默认权限"
empower_default $case17
touch $file_name/test02/case3.sh
prove2 $case17

case18="-w-"
rm -rf $file_name/test02/case3.sh
clear_all_acl $file_name
echo "case18默认递归赋予wang $case18 ACL权限，验证创建的文件继承默认权限"
empower_default $case18
touch $file_name/test02/case3.sh
prove2 $case18

case19="--x"
rm -rf $file_name/test02/case3.sh
clear_all_acl $file_name
echo "case19默认递归赋予wang $case19 ACL权限，验证创建的文件继承默认权限"
empower_default $case19
touch $file_name/test02/case3.sh
prove2 $case19

case20="r-x"
rm -rf $file_name/test02/case3.sh
clear_all_acl $file_name
echo "case20默认递归赋予wang $case20 ACL权限，验证创建的文件继承默认权限"
empower_default $case20
touch $file_name/test02/case3.sh
prove2 $case20

case21="-wx"
rm -rf $file_name/test02/case3.sh
clear_all_acl $file_name
echo "case21默认递归赋予wang $case21 ACL权限，验证创建的文件继承默认权限"
empower_default $case21
touch $file_name/test02/case3.sh
prove2 $case21
dang1

#清除用户权限
case22="rwx"
echo "case22 验证指定文件/目录 用户权限 清除命令是否生效"
clear_all_acl $file_name
empower_recs $case22
clear_user_acl wang $file_name
clear_user_acl wang $file_name/test02/case1.sh
prove4 $case22

#清除所属组权限
case23="rwx"
echo "case23 验证指定文件/目录 用户组权限 清除命令是否生效"
clear_all_acl $file_name
empower_group $case23 
clear_group_acl wang2 $file_name
clear_group_acl wang2 $file_name/test02/case1.sh
prove5 $case23

