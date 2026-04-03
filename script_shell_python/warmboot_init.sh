#!/bin/bash
#b=1
#if [[ $# -lt 1 ]]
#then
#	echo "usage : $0 100"
#        exit 0
#fi
#sudo dbus-send --system --print-reply --dest=com.deepin.daemon.Accounts /com/deepin/daemon/Accounts/User1000 com.deepin.daemon.Accounts.User.SetAutomaticLogin boolean:true

apt install -y zenity &>/dev/null
reboot_count=$(zenity --title="循环次数" --text "请输入循环次数" --entry)
reboot_core=`/usr/bin/realpath $0`
reboot_path=`/usr/bin/dirname $reboot_core`
reboot_run=$reboot_path"/warmboot_run.sh"
reboot_desktop=$HOME/.config/autostart

if [ ! -d $reboot_path ]
then
	echo "Not Found warmboot_init.sh"
	exit 0
fi

if [ ! -d $reboot_desktop ]
then
	/bin/mkdir -p $reboot_desktop
fi
dd of=$reboot_run << EOF
#!/bin/bash
basepath=$reboot_path
count=$reboot_count
b=1
if [[ -e \$basepath/times.log ]]
then

        a=\`cat \$basepath/times.log\`
        if [[ \$a -gt \$count ]]
        then
                exit 2
        else
                ct=\`expr \$a + \$b\`
                echo "\$ct" > \$basepath/times.log
                echo "\$ct" >> \$basepath/times-full.log
                echo "\`date\`">> \$basepath/times-full.log
                if [[ ! -d \$basepath/logs ]]
                then
                        /bin/mkdir -p \$basepath/logs
                fi
                #/bin/journalctl > \$basepath/logs/log"\`date +%Y%m%d\`".\$a
                 /bin/journalctl | egrep "error|failed|warning" >> \$basepath/logs/log
                echo "--------------------------------------------" >> \$basepath/logs/log
                sleep 12
                browser  https://v.qq.com/x/cover/bzfkv5se8qaqel2/w0034zvw8ky.html &
                sleep 60
                /sbin/reboot
        fi

else
        touch \$basepath/times.log
        echo "1" > \$basepath/times.log

fi
EOF
/bin/chmod +x $reboot_run

dd of=$reboot_desktop/reboot-test.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Exec=/usr/bin/bash $reboot_run
Terminal=false
Type=Application
Name[en_US]=reboot$reboot_count
EOF

/bin/chmod +x $reboot_desktop
sleep 5
chmod 777 warmboot_run.sh
./warmboot_run.sh
./warmboot_run.sh
