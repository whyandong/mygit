#! /bin/bash
set -x 

dir=getlog
mkdir -p $dir
cp -f /var/log/messages $dir
cp -f /var/log/Xorg* $dir
cp -rf /var/log/journal $dir
cp -rf /var/log/kern.log $dir
cp -f /home/$USER/kwin.log $dir
cp -rf /var/lib/systemd/coredump $dir

uname -a > $dir/uname.log
mount > $dir/mount.log
lspci -nn > $dir/lspci.log
lsusb -v >$dir/lsusb.log


tar -zcvf  log.tar.gz $dir
rm -rf $dir