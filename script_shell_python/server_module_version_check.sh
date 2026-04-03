#! /bin/bash
#预制清单填到下面括号中，空格分开
package=(systemd libpam-systemd libsystemd0 systemd-coredump xserver-xorg-core xserver-common xserver-xephyr deepin-ab-recovery deepin-license-activator dde-wloutput-daemon dde-wldpms dde-wloutput dde-api dde-daemon startdde libkf5waylandserver5 libkf5waylandclient5 kwayland-data dde-session-shell dde-launcher dde-introduction deepin-music deepin-screen-recorder deepin-image-viewer dde-desktop dde-disk-mount-plugin dde-file-manager kelvinu dde-device-formatter dde-kwin deepin-devicemanager deepin-desktop-schemas deepin-log-viewer grub-common grub-efi-arm64 grub-efi-arm64-bin grub2-common dde-control-center dde-session-ui libdtkcore5 libdtkcore5-bin libdtkwidget5 libdtkwidget5-bin deepin-manual dde-dock deepin-shortcut-viewer deepin-compressor deepin-voice-note gparted smartpa policykit-1 gir1.2-polkit-1.0 libpolkit-agent-1-0 libpolkit-backend-1-0 libpolkit-gobject-1-0 deepin-app-store deepin-app-store-data libcogl-pango20 libcogl-path20 libcogl20 gir1.2-gtk-3.0 gtk-update-icon-cache libgtk-3-0 libgtk-3-common totem gir1.2-totem-1.0 libtotem0 totem-common totem-plugins)
for data in ${package[@]}
do
	echo ${data}
	a=`apt-cache policy ${data}| awk '{print $1}' | grep 已安装`
	if [ ! -n "$a" ];then
		echo "未发现${data}版本"
	else
		echo "当前系统安装版本：$a"
	fi
done
