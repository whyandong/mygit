#!/bin/bash
#获取当前运行工程目录
script_path="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd  )"
#切到环境配置脚本目录
cd $script_path/resource/tools/auto_envion_deploy/
#进行仓库重配置，防止更新失败
echo 1|sudo -S dpkg --configure -a
echo 1|sudo -S rm /var/lib/dpkg/updates/*
#进行系统仓库更新，获取更新包
echo 'apt-get update***********************************'
echo '1' | sudo -S apt-get update
# echo 'apt-get 离线安装deb包***********************************'
# dpkg离线包下载
# sudo apt install -d python3-pip python3-tk python3-dev python3-pyatspi python3-pyqt5 xclip scrot python3-opencv ntpdate -y
# ls -la /var/cache/apt/archives
# mv /var/cache/apt/archives ${somewhere}
# echo '1' | sudo -S dpkg -i *.deb
# python离线包下载
# sudo pip3 download pytest==6.2.2 allure-pytest==2.8.36 pyautogui==0.9.52 selenium==3.141.0
# echo 'apt-get 离线安装python包(whl)***********************************'
# echo '1' | sudo -S pip3 install --force-reinstall *.whl
# 修改系统python为python3
echo 1|sudo -S cp /usr/bin/python3.7 /usr/bin/python
# 安装pip3
echo 1|sudo -S apt install python3-pip -y
# 安装allure-pytest与openpyxl
echo 1 |sudo -S pip3 install openpyxl
# 安装并配置git
# echo 1|sudo -S apt install -y git
# git config --global user.name "ut002037"
# git config --global user.email wangxiaogang@uniontech.com
# echo 1|sudo -S apt install libffi-dev -y
# pip3 install paramiko
# pip3 install configparser

# echo 'apt-get 离线安装deb包(tar)***********************************'
# for PACKAGE in *.tar.gz
# do
# 	cd $script_path/resource/tools/auto_envion_deploy/packages_ci_env
# 	tar -zxvf $PACKAGE
# 	cd ./${PACKAGE%.t*}
# 	echo '1' | sudo -S python3 setup.py install
# done

# 离线安装allure
cd $script_path/resource/tools/auto_envion_deploy;echo '1' | sudo -S bash auto_envion_deploy.sh
export PATH=$PATH:/usr/bin/allure/bin
# 离线安装dogtail
# cd $script_path/resource/tools/auto_envion_deploy/dogtail
# echo '1' | sudo -S python3 setup.py install
#返回原始目录
cd $script_path
# #重启lightdm
# echo "1" | sudo -S systemctl restart lightdm.service
