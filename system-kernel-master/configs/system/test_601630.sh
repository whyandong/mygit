#!/bin/bash
if [ $1 = "amd64" ];then
        cd /boot/efi/EFI;md5sum */*|grep grub.efi|awk '{print $1}'
        cd /boot/efi/EFI;md5sum */*|grep shimx64.efi|awk '{print $1}'
elif [ $1 = "arm64" ];then
        cd /boot/efi/EFI;md5sum */*|grep shimaa64.efi|awk '{print $1}'
        cd /boot/efi/EFI;md5sum */*|grep grubaa64.efi|awk '{print $1}'
fi