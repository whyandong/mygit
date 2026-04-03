一、在/etc/下创建rc.local文本
sudo touch /etc/rc.local
sudo chmod -R 777 /etc/rc.local

二、编写内容
sudo vim /etc/rc.local

#!/bin/sh -e
sleep 1
sudo ./xxx.sh
exit 0

三、重启Ubuntu
sudo reboot
