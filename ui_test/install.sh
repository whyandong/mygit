#!/bin/bash
if [ `id -u` -ne 0 ]; then
	echo "**********************************************************"
	echo -e  "\033[31m请使用 sudo 权限执行该脚本，谢谢！\033[0m"
	echo "**********************************************************"
	exit 0
fi

# ping wwww.baidu.com -c 3 > /dev/null 2>&1

# if [ $? -ne 0 ]; then
#     echo -e "\033[31m需要连接外网，谢谢！\033[0m"
#     exit 1
# fi

which python3 > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo -e "\033[31m需要安装python3，谢谢！\033[0m"
    exit 1
fi

dpkg -l python3-pip |grep ii
if [ $? -ne 0 ]; then
    echo -e "\033[32m python3-pip \033[0m"
    dpkg -i ./pip3deb/*.deb
fi
dpkg -l python3-pip |grep ii
dir_name=$(pwd)
cd ${dir_name}/package
if [ $? -eq 0 ]; then
    echo -e "\033[32m  安装接口自动化依赖包 \033[0m"
    pip3 install --no-index --find-links=. -r ../requirements_offline.txt
# pip3 install -r requirement.txt
fi

if [ -e /usr/local/lib/python3.9/dist-packages/pytest_html ]; then
   rm -rf /usr/local/lib/python3.9/dist-packages/pytest_html/resources
   rm -rf /usr/local/lib/python3.9/dist-packages/pytest_html/plugin.py
   mv ${dir_name}/resources /usr/local/lib/python3.9/dist-packages/pytest_html/
   mv ${dir_name}/plugin.py /usr/local/lib/python3.9/dist-packages/pytest_html/
else
   echo -e "\033[31m pytest-html 未正常安装 \033[0m"
fi