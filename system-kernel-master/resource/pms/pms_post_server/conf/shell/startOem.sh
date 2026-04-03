###
 # @Author: zhuzhou@uniontech.com
 # @Date: 2021-04-21 11:10:34
 # @LastEditTime: 2021-04-21 11:10:34
### 
#!/bin/bash


procnum=`ps -ef|grep FileMonitor.py|grep -v grep|wc -l`
if [ $procnum -eq 0 ]; then
    cd /home/uos/oem_auto
    python3 FileMonitor.py &
fi  

