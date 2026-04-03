#!bin/bash
#pxe支撑软件安装
apt update

n=`apt-cache policy debian-installer-10-netboot-mips64el |grep '已安装' |cut -c 16-18`
if [ $n = '无' ];then
	apt install  debian-installer-10-netboot-mips64el -y 
fi

d=`apt-cache policy dnsmasq |grep '已安装' |cut -c 16-18`
if [ $d = '无' ];then
	apt install  dnsmasq -y 
fi

nf=`apt-cache policy nfs-kernel-server |grep '已安装' |cut -c 16-18`
if [ $nf = '无' ];then
	apt install  nfs-kernel-server -y 
fi

ne=`apt-cache policy net-tools |grep '已安装' |cut -c 16-18`
if [ $ne = '无' ];then
	apt install  net-tools -y 
fi

#NFS配置

if [ -a /var/nfs ]
then
    
    rm -rf /var/nfs
fi
mkdir /var/nfs

#截取exports倒数第一行的第一位到第八位字符
n=$(tail -n 1 /etc/exports |cut -c 1-8)
if [ $n = '/var/nfs' ]
then
   echo 'NFS已配置'
else
   echo '/var/nfs *(ro,sync,no_subtree_check)' | tee -a /etc/exports
fi

systemctl restart nfs-kernel-server
mkdir -p /var/nfs/mips64el
i=$(find *.iso)
if [ ! -n "$i" ]; then
   echo -e "\033[4;31m 没有检测到镜像文件，请将镜像放到pxe文件夹中！然后重新执行脚本 \033[0m"
   sleep 1
   exit
  
fi
chmod 777 *.iso
mount *.iso /mnt/
cp -r /mnt/* /var/nfs/mips64el/
cp -r /mnt/.disk/ /var/nfs/mips64el/
chown -R root:root /var/nfs/
find /var/nfs/mips64el/ -type d -exec chmod 755 {} \;

#TFTP配置
if [ -a /var/tftp ]
then
    
    rm -rf /var/tftp
fi


mkdir /var/tftp
mkdir -p /var/tftp/debian-installer/efi-mips64el/grub/
touch /var/tftp/debian-installer/efi-mips64el/grub/grub.cfg
mkdir -p /var/tftp/debian-installer/live-mips64el
cp core.efi /var/tftp/debian-installer/efi-mips64el
cp -r grub2 /var/tftp/
cp -r /mnt/live /var/tftp/debian-installer/live-mips64el/
cp  /mnt/boot/vmlinuz /var/tftp/debian-installer/live-mips64el/live
cp /mnt/boot/initrd.img /var/tftp/debian-installer/live-mips64el/live
chmod 777 /var/tftp/grub2
chmod 777 /var/tftp/grub2/grub.cfg
cat grub.txt  > /var/tftp/grub2/grub.cfg
cat grub.txt  > /var/tftp/debian-installer/efi-mips64el/grub/grub.cfg


group='dnsmasq'
egrep "^$group" /etc/group >& /dev/null  
if [ $? -ne 0 ]  
then  
   groupadd $group  
fi  

chown dnsmasq:dnsmasq /var/tftp -R

#Dnsmasq配置
#获取连接网卡名称,获取第六列第二行到第二行
a=$(cat /proc/net/arp | sed -n '2,2p' | awk '{print $6}')
  
if [ ! -n "$a" ]; then
   echo -e "\033[4;31m 网络不通，请插上网线！然后重新执行脚本 \033[0m"
   sleep 1
   exit
  
else
  
   sed -i "s/enp2s0/${a}/g" `grep enp2s0 -rl ./` 
  
fi


chmod 777 /etc/network/interfaces
b=$(tail -n 1 /etc/network/interfaces |cut -c 1-8)
if [ $b = 'gateway' ]
then
   echo '网络已配置'
else
   cat dnsmasq.txt  >> /etc/network/interfaces
fi

systemctl restart NetworkManager
chmod 777 /etc/dnsmasq.conf

sed '680,$d' -i   /etc/dnsmasq.conf 

cat dnsmas.txt  >> /etc/dnsmasq.conf


systemctl restart dnsmasq


echo 'pxe已配置完成'
reboot
