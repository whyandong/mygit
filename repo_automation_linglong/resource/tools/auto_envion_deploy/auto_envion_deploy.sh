#!bin/bash
#dbus自动化环境部署

folder=/usr/bin/allure

sudo apt-get install python3-pip -y

sudo apt-get install git -y

if [ ! -d $folder ];then

    tar zxvf allure-2.13.5.tgz

    sudo mv allure-2.13.5 /usr/bin/allure

    echo '安装allure'
else
    
    echo 'allure已安装'
fi

if grep -q "allure" /etc/profile;then
    echo '环境变量已存在'
else
    sudo sh -c 'echo export PATH=\$PATH:/usr/bin/allure/bin >> /etc/profile'
    echo '添加环境变量'
fi

sudo pip3 install -r requestment.txt

source /etc/profile

source ~/.bashrc

sudo apt install openjdk-8-jdk -y

