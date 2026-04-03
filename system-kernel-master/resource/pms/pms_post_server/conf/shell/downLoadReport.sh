###
 # @Author: lihea@uniontech.com
 # @Date: 2020-09-10 11:10:34
 # @LastEditTime: 2020-10-14 11:19:31
### 
#!/bin/bash

wget -P /home/uos/report $1
cd /home/uos/report
unzip *.zip
rm -rf *.zip
mv /home/uos/report/* test