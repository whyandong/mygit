#! /bin/bash
if [ -n "/usr/bin/coredumpctl" ];then
		echo -e "\e[031m 未发现coredumpctl,请root权限运行以下命令，普通用户运行本脚本 \e[0m"
        echo -e "\e[031m sudo apt install systemd-coredump  -y \e[0m"
		exit 2   
fi
number=50 #输入需要压测的循环次
num=1
DATE=$(date +"%Y-%m-%d %H:%M:%S")
#预制清单填到下面括号中，空格分开
package=(uos-browser dde-file-manager \/opt\/apps\/org\.deepin\.scanner\/files\/scanner\/bin\/EFileApp\.sh \/opt\/apps\/org\.deepin\.chineseime\/files\/bin\/chinime-setw deepin-app-store deepin-music deepin-movie deepin-screen-recorder deepin-image-viewer deepin-album deepin-draw deepin-reader deepin-editor thunderbird deepin-terminal deepin-contacts deepin-voice-note deepin-manual dde-control-center fcitx-configtool deepin-defender deepin-boot-maker deepin-devicemanager deepin-log-viewer dde-printer dde-calendar deepin-calculator deepin-font-manager deepin-compressor deepin-deb-installer deepin-diskmanager dde-introduction uos-service-support deepin-camera)

check_default_app(){
for data in ${package[@]}
do
	echo ${data}
    if [ $data == 'uos-browser' ]; then 
    a=`apt-cache policy uos-browser-stable | awk '{print $1}' | grep 已安装`
    elif [ $data == 'fcitx-configtool' ];then  
    a=`apt-cache policy fcitx-config-common | awk '{print $1}' | grep 已安装`
    elif [ $data == '/opt/apps/org.deepin.scanner/files/scanner/bin/EFileApp.sh' ];then  
    echo -e "\e[031m Warning 扫描仪以脚本运行，可尝试以下命令运行后确认版本信息\
   bash /opt/apps/org.deepin.scanner/files/scanner/bin/EFileApp.sh  \e[0m"
    elif [ $data == '/opt/apps/org.deepin.chineseime/files/bin/chinime-setw' ];then  
    echo -e "\e[031m Warning 中文输入法设置向导，可尝试以下命令运行后确认版本信息\
   \/opt\/apps\/org\.deepin\.chineseime\/files\/bin\/chinime-setw  \e[0m"
    else
	a=`apt-cache policy ${data}| awk '{print $1}' | grep 已安装`
    fi

	if [ ! -n "$a" ];then
		echo -e "\e[031m 未发现${data}版本 \e[0m"
		echo -e "\e[031m Warning 请确认 预装列表中 ${package[@]} 是否已安装 \e[0m"
		exit 2
	fi
done
}
check_crash(){
a=`coredumpctl list | awk '{print $10}'` 
if [ ! -n "$a" ];then
echo -e "\e[030m 未发现crash event Case FASS \e[0m"
else
echo -e "\e[031m Case Fail 存在crash event $a \e[0m"
fi
}
default_app_Pressure_test(){
for data in ${package[@]}
do
	echo ${data}
	if [ $data == '/opt/apps/org.deepin.scanner/files/scanner/bin/EFileApp.sh' ]; then 
	bash /opt/apps/org.deepin.scanner/files/scanner/bin/EFileApp.sh  &	
    elif [ $data == '/opt/apps/org.deepin.scanner/files/scanner/bin/EFileApp.sh' ]; then 
    \/opt\/apps\/org\.deepin\.chineseime\/files\/bin\/chinime-setw &
	else
	$data & 
	fi
	sleep 5
    if [ $data == 'deepin-terminal' ];then
    echo "app is deepin-terminal so skip "
    elif [ $data == 'uos-browser' ];then 
    	kill -9 `ps -ef | grep uosbrowser | awk '{print $2}'`
    elif [ $data == 'fcitx-configtool' ];then 
    	kill -9 `ps -ef | grep fcitx-config-gtk3 | awk '{print $2}'`
    elif [ $data == '/opt/apps/org.deepin.scanner/files/scanner/bin/EFileApp.sh' ];then 
    	kill -9 `ps -ef | grep EFileApp | awk '{print $2}'`
    elif [ $data == '\/opt\/apps\/org\.deepin\.chineseime\/files\/bin\/chinime-setw' ];then 
    	kill -9 `ps -ef | grep chinime-setw | awk '{print $2}'`
    else
    kill -9 `ps -ef | grep $data | awk '{print $2}'`
    fi
done
}
check_default_app 
while true
do 
default_app_Pressure_test >> ./log
echo 第 "$num"次测试。。。
num=`expr $num + 1 `
if [ $num -gt $number ];then
times=`expr $num - 1 `
echo 完成待机测试，总共$times次。
break
fi 
done
check_crash
