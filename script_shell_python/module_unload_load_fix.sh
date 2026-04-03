#!/bin/bash

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright: 2016 IBM
# Author: Harsha Thyagaraja <harshkid@linux.vnet.ibm.com>

#编译生成可直接调用模块 -y builtin module
CONFIG_FILE=./old.config
BUILT_IN_DRIVERS=`cat /lib/modules/$(uname -r)/modules.builtin |awk -F"/" '{print $NF}'|sed 's/\.ko//g'`
if [[ $MODULES ]]; then
    DRIVERS=`echo $MODULES | sed 's/,/ /g'`
elif [[ $ONLY_IO == True ]]; then
#PCI占用驱动,无法被卸载
    DRIVERS=`lspci -k | grep -iw "Kernel driver in use" | cut -d ':' -f2 | sort | uniq`
else
#额外模块需加载后使用 -m   external module  
    DRIVERS=`find /lib/modules/$(uname -r)/ -name \*.ko | awk -F"/" '{print $NF}'|grep -v "^mlx5" | grep -v "^mlx4" |sed 's/\.ko//g'`
fi
ERR=""
PASS=""
[[ -z $ITERATIONS ]] && ITERATIONS=10


module_load() {
    modprobe $1
    if [[  $? != 0  ]]; then
        echo "Failed to load driver module $1"
        ERR="$ERR,load-$1"
        break;
    fi
    echo "Reloaded driver $1"
    for i in $( cat $CONFIG_FILE | grep "$1=" | awk -F'=' '{print $2}' ); do
        module_load $i
        if [[  $? != 0  ]]; then
            return
        fi
    done
}


module_unload() {
    for i in $( cat $CONFIG_FILE | grep "$1=" | awk -F'=' '{print $2}' ); do
        module_unload $i
        if [[  $? != 0  ]]; then
            return
        fi
    done
    echo "Unloaded driver $1"
    rmmod $1
    if [[  $? != 0  ]]; then
        echo "Failed to unload driver module $i"
        ERR="$ERR,unload-$1"
        break;
    fi
}
#检查默认挂载的模块一致性
builtin_chek(){
	cat /lib/modules/$(uname -r)/modules.builtin |awk -F"/" '{print $NF}'|sed 's/\.ko//g' > ./a.config
        if [ ! -f ./old.config ]; then
                echo defeault knrnel buitin module conf nor exist 
                                exit 2
        else
                a=`sort a.config old.config old.config | uniq -u` 
                if [ -z "$a" ]  ; then
                        echo defeault knrnel buitin module check : PASS 
                        echo 
                        sleep 2
                else
                echo warning : new add knrnel module new $a
                fi
        fi
}

sleep 5
echo ` lspci -k | grep -iw "Kernel driver in use" | cut -d ':' -f2 | sort | uniq `
echo driver in use from PCI ,  builtin and it cannot be unloaded
builtin_chek
echo test  goon .... 

for driver in $DRIVERS; do
    echo "Starting driver module load/unload test for $driver"
    echo
     #如果包含PCI正常调用的驱动,直接跳过验证
        if [[ `lspci -k | grep -iw "Kernel driver in use" | cut -d ':' -f2 | sort | uniq` =~ "$driver" ]]; then
                echo $driver in `lspci -k | grep -iw "Kernel driver in use" | cut -d ':' -f2 | sort | uniq`
		echo Kernel driver in use from PCI ,  builtin and it cannot be unloaded
                #break;
        else
                echo $driver
        fi

    for j in $(seq 1 $ITERATIONS); do
        echo $BUILT_IN_DRIVERS | grep -w $driver > /dev/null
        if [[ $? == "0" ]]; then
            echo $driver" is builtin and it cannot be unloaded"
            break;
        fi
        #vfs_monitor模块挂载会卡住， 这里手动进行过滤
        if [[ $driver == "vfs_monitor" ]]; then
            echo $driver" vfs_monitor is  skip"
            break;
        fi
		#如果已加载的模块不予进行测试
        if [[ $(lsmod | grep -w ^$driver | awk '{print $NF}') != '0' ]]; then
            if [[ $(grep "$driver=" $CONFIG_FILE > /dev/null; echo $?) != '0' ]]; then
                echo $driver" has dependencies and it cannot be unloaded"               
                break;
            fi
        fi
        module_unload $driver
        # Sleep for 5s to allow the module unload to complete
        sleep 5
        module_load $driver
        # Sleep for 5s to allow the module load to complete
        sleep 5
        echo
    done
    if [[  $j -eq $ITERATIONS  ]]; then
        PASS="$PASS,$driver"
    fi
    echo
    echo "Completed driver module load/unload test for $driver"
    echo
done
echo
if [[  "$ERR"  ]]; then
    echo "Some modules failed to load/unload: ${ERR:1}"
    exit 1
fi
if [[  "$PASS"  ]]; then
    echo "Successfully loaded/unloaded: ${PASS:1}"
fi

