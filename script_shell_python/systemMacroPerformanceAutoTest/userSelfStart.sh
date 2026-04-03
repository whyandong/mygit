#!/bin/bash

sleep 15


export DISPLAY=:0

xdotool key alt+ctrl+t
# dbus-send --session --print-reply --dest=com.deepin.SessionManager /com/deepin/StartManager com.deepin.StartManager.Launch string:/usr/share/applications/deepin-terminal.desktop

sleep 2

xdotool type 'cd /home/uos/systemMacroPerformanceAutoTest'

xdotool key Return

function off_acpi_manager(){
    # 设置待机时间为从不
	xdotool type 'dbus-send --session --dest=com.deepin.daemon.Power --print-reply /com/deepin/daemon/Power org.freedesktop.DBus.Properties.Set string:com.deepin.daemon.Power string:LinePowerSleepDelay variant:int32:0'
	xdotool key Return
	sleep 1
    # 设置锁定时间为从不
	xdotool type 'dbus-send --session --dest=com.deepin.daemon.Power --print-reply /com/deepin/daemon/Power org.freedesktop.DBus.Properties.Set string:com.deepin.daemon.Power string:LinePowerLockDelay variant:int32:0'
	xdotool key Return
	sleep 1
    # 设置锁定时间为从不
	xdotool type 'dbus-send --session --dest=com.deepin.daemon.Power --print-reply /com/deepin/daemon/Power org.freedesktop.DBus.Properties.Set string:com.deepin.daemon.Power string:LinePowerScreenBlackDelay variant:int32:0'
	xdotool key Return
	sleep 1
    # 关闭待机唤醒时需要密码
    xdotool type 'dbus-send --session --print-reply --dest=com.deepin.daemon.Power /com/deepin/daemon/Power org.freedesktop.DBus.Properties.Set string:com.deepin.daemon.Power string:SleepLock variant:boolean:false'
	xdotool key Return
	sleep 1
    # 关闭休眠唤醒时需要密码
    xdotool type 'dbus-send --session --print-reply --dest=com.deepin.daemon.Power /com/deepin/daemon/Power org.freedesktop.DBus.Properties.Set string:com.deepin.daemon.Power string:ScreenBlackLock variant:boolean:false'
	xdotool key Return
	sleep 1
	echo "1" > /home/uos/pressure_test/set.txt

}

if [ ! -f "/home/uos/systemMacroPerformanceAutoTest/set.txt" ];then
    off_acpi_manager
fi

xdotool type 'bash autoTest.sh'
xdotool key Return