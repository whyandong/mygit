###
 # @Author: hancheng@uniontech.com
 # @Date: 2020-09-10 11:10:34
 # @LastEditTime: 2020-10-14 11:19:31
### 
#!/bin/bash

tempPath=/home/uos/iso_daily/temp

#如果文件夹不存在则创建                                                                                                                                                                                              
if [ ! -d $tempPath ];                                                                                                                                                                                             
then                                                                                                                                                                                                                 
    mkdir -p $tempPath;                                                                                                                                                                                            
fi    

wget -P $tempPath $1

mv $tempPath/$2.iso /home/uos/iso_daily/$3.iso
