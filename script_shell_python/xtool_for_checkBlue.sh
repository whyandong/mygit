#! bin/bash
#[[ $EUID -ne 0 ]] && echo 'Error: This script must be run as root!' && exit 1
expected_MD5="3657d87308ab64ad569c38e65789f7cd"
filename="10000-socket.tar.gz"
check_path=/home/uos/Downloads
DATE=$(date +"%Y-%m-%d %H:%M:%S")
check_bule(){
while true 
	do xdotool mousemove 1208 42 click 1 
	sleep 20
done
}

check_file(){
	while true
	do
	sleep 5	
	if [ ! -f $check_path/$filename ]; then
		echo check go on .... $DATE 
	else	
		ss=`md5sum $check_path/$filename | awk '{print $1}'`
		cat $ss >> $check_path/log
		cat $expected_MD5 >> $check_path/log
		if [ "$ss" != "$expected_MD5" ]
       			then
  			echo  ERR : file $ss !=  incomplete $DATE >> $check_path/log
			mv $check_path/$filename /tmp/$filename$DATE
	      		exit 2
        	else
               	echo Pass : file complete  >> $check_path/log
		rm -rf $check_path/$filename 
        #kill -9 `ps -ef | grep "/usr/bin/dde-file-manager-daemon" | awk '{print $2}'`
        	fi
	fi
	done

}
	check_bule &
	check_file &
