###
 # @Author: zhuzhou@uniontech.com
 # @Date: 2020-12-29 14:28:41
### 
#!/bin/bash

project_path=$(cd `dirname $0`; pwd)
conf=$project_path/conf.ini
user_passwd=`sed '/^passwd = /!d;s/.*= //' $conf`

isoPath="/var/nfs/isoList/$2/$1"

sudoCommand(){
    echo $user_passwd | sudo -S $1
}

sudoCommand "rm $isoPath -r"
