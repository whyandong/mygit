###
 # @Author: zhuzhou@uniontech.com
 # @Date: 2021-04-21 11:10:34
 # @LastEditTime: 2021-04-21 11:10:34
### 
#!/bin/bash

procnum=`ps -ef|grep api_server|grep -v grep|wc -l`
if [ $procnum -eq 0 ]; then
    cd /home/uos/auto_platform
    ./api_server &
fi  