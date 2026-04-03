#! /bin/bash
#预制清单填到下面括号中，空格分开
package=(libegl-mesa0 libgl1-mesa-dri libgl1-mesa-glx libglapi-mesa libglu1-mesa libglx-mesa0 mesa-va-drivers mesa-vdpau-drivers linux-firmware intelgpu-dkms grub-efi-amd64-signed libdrm-intel1 libdrm-nouveau2 libdrm-radeon1 libegl1 libgl1 libgles2 libglvnd0 libglx0)
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
