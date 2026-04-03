#!/bin/bash

sleep 15


export DISPLAY=:0

xdotool key alt+ctrl+t

echo "用户自启成功"

if [ ! -f "/home/uos/.config/autostart/test.desktop" ];then
    cat > "/home/uos/.config/autostart.desktop" << EOF
[Desktop Entry]
Name=portTest
Exec=/home/uos/userSelfStart.sh
Type=Application
EOF
    echo "自启配置写入成功"
fi

