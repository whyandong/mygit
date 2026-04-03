#!/bin/bash 
source /etc/profile
#加载环境变量
if [ -f ~/.bash_profile ];
then
  . ~/.bash_profile
fi
#安装路径配置
file_name=redis
#输入redis常用配置信息
read -p "Input redis software redis_path. (For example: /usr/loacl) " redis_path
read -p "Input redis software ip. (For example: 192.168.1.71) " new_redis_ip
read -p "Input redis software connection passwd. (For example: 12345isa) " new_redis_passwd
read -p "Input redis software connection port. (For example: 6379) " new_redis_port
#获取老的配置信息
old_redis_ip=`/usr/bin/sed -n '69p' /$redis_path/redis/redis.conf | awk '{print $2}'`
old_redis_port=`/usr/bin/sed -n '92p' /$redis_path/redis/redis.conf | awk '{print $2}'`
old_redis_passwd=`/usr/bin/sed -n '500p' /$redis_path/redis/redis.conf | awk '{print $2}'`
#判断是否已存在该目录,若存在也提示是否删除目录安装，否则退出脚本
if [ -d "$redis_path/$file_name"]; then
    read -p "Input You want to [目录已存在，确认是否删除！Yes （删除原目录继续安装）输入其他任意值 （退出本次脚本部署]）" answer
   if ["$answer"!="yes"]; then
    break
    else
   rm -rf $redis_path/$file_name
    sleep 3
    echo "安装目录下未发现redis目标，执行安装！" 
   else
    unzip redis.zip /$redis_path
#安装namp命令
rpm -ivh $redis_path/redis/nmap-7.60-1.x86_64.rpm
sleep 10
#配置redis后台运行
sed -i 's/daemonize no/daemonize yes/g' /$redis_path/redis/redis.conf
#配置日志信息
mkdir /$redis_path/redis/log
sed -i 's#logfile ""#logfile "/usr/local/redis/log/redis.log"#g' /$redis_path/redis/redis.conf
#备份配置文件
mkdir /etc/redis
cp $redis_path/redis/redis.conf /etc/redis/6379.conf
#配置redis访问IP
sed -i 's/old_redis_ip/new_redis_ip/g' /$redis_path/redis/redis.con
#配置redis访问密码
sed -i 's/old_redis_passwd/new_redis_passwd/g' /$redis_path/redis/redis.conf
#配置redis访问端口
sed -i 's/old_redis_port/new_redis_port/g' /$redis_path/redis/redis.conf
#加入开机自启动
cp $redis_path/redis/redis_init_script /etc/init.d/redisd
echo "# chkconfig:   2345 90 10" >> /etc/init.d/redisd
echo "# description:  Redis is a persistent key-value database" >> /etc/init.d/redisd
chkconfig redisd on
#启动redis
chmod 777 /$redis_path/redis/bin/redis-server 
chmod 777 /$redis_path/redis/bin/redis-cli
/$redis_path/redis/bin/redis-server  /$redis_path/redis/redis.conf
#加入定时监测脚本
echo "*/1 * * * * sh /$redis_path/redis/redisMonitor.sh >> /mnt/redismonitor.log" >> /var/spool/cron/root
echo "* * 1 * * sh /$redis_path/redis/delete_redis_log.sh >> /mnt/redis_clear_monitor.log" >> /var/spool/cron/root
sleep 5
echo "Deployment completed!"   
 if
if

done

