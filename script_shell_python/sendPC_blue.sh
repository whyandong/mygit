#! /bin/bash
read -p "请输入需要测试文件：（如：/home/uos/111.txt）" filepath
sleep 1
hcitool scan
sleep 2
read -p "请输入已建立蓝牙连接的设备MAC地址：（如：F4:B7:E2:E9:9F:11）" MAC

echo loop forver , if you want stop , you can use  CTRL + Z
send_blue_file(){
	while true 
	do
	dbus-send --print-reply --session --dest=com.deepin.daemon.Bluetooth /com/deepin/daemon/Bluetooth com.deepin.daemon.Bluetooth.SendFiles  string:$MAC array:string:$filepath
	sleep 600
	done
}
	send_blue_file
