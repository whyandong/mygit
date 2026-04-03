###
 # @Author: zhuzhou@uniontech.com
 # @Date: 2020-12-29 14:28:41
### 
#!/bin/bash

project_path=$(cd `dirname $0`; pwd)
conf=$project_path/conf.ini
user_passwd=`sed '/^passwd = /!d;s/.*= //' $conf`

linkPath="/var/nfs/$2"

sudoCommand(){
    echo $user_passwd | sudo -S $1
}

if [ -L "$linkPath" ]; then       #如果软连接存在，则将其删除重新创建
  sudoCommand "rm $linkPath"
fi

sudoCommand "ln -s /var/nfs/isoList/$2/$1 $linkPath"