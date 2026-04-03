#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          459293<-----475229
# @Test Description:      检查grub和内核文件的签名情况
# @Test Condition:       安装sbsigntool
# @Test Step:           1.检查系统是否为1040 amd64架构 2.检查内核文件是否签名 3.检查grub文件是否签名 4.检查grubx文件是否签名
# @Test expect Result:  1.若是1040系统amd64架构，继续执行；若不是忽略此条用例  2.检查内核文件已经签名 3.grub文件已经签名 4.grubx文件已经签名
# @Test Remark:
# @Author:  夏曙_ut000220
# *****************************************************
import sys
import os
import pytest
import logging

from frame.common import system_kernel_log_cap, get_platform_arch


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    os.system("echo 1|sudo -S apt install sbsigntool -y")
    yield
    os.system("echo 1 |sudo -S apt remove sbsigntool --purge -y")
    os.system("echo 1|sudo -S rm -rf /home/uos/vmlinuz.gz")
    os.system("echo 1|sudo -S rm -rf /home/uos/vmlinuz")


def iso_install_mode():
    '''
    判断系统安装模式是否为efi安装,如果存在efi文件夹,则为efi安装
    '''
    if os.path.exists("/sys/firmware/efi"):
        return True
    else:
        return False


@pytest.mark.skipif(iso_install_mode() is False, reason="legacy安装不走安全启动流程!")
def test_vmlinuxz_grubx_signature_459293():
    if "amd" in get_platform_arch():
        # 内核签名信息
        linuz_sig = os.popen(
            "echo 1|sudo -S sbverify --list /boot/vmlinuz-4.19.0-amd64-desktop | grep 'UOS APP Signing CA'"
        ).read()
        # grub签名信息
        grub_sig = os.popen(
            "echo 1|sudo -S sbverify --list /boot/efi/EFI/UOS/grubx64.efi | grep 'UOS APP Signing CA'"
        ).read()
        # shim签名信息
        shim_sig1 = os.popen(
            "echo 1|sudo -S sbverify --list /boot/efi/EFI/UOS/shimx64.efi | grep 'Microsoft'"
        ).read()
        shim_sig2 = os.popen(
            "echo 1|sudo -S sbverify --list /boot/efi/EFI/UOS/shimx64.efi |grep 'Uniontech UEFI CA'"
        ).read()
        shim_sig = shim_sig1 + shim_sig2

        # 如下是debug信息，失败时候打印
        linuz_sig_debug = os.popen(
            "echo 1|sudo -S sbverify --list /boot/vmlinuz-4.19.0-amd64-desktop"
        ).read()
        grub_sig_debug = os.popen(
            "echo 1|sudo -S sbverify --list /boot/efi/EFI/UOS/grubx64.efi"
        ).read()
        shim_sig_debug = os.popen(
            "echo 1|sudo -S sbverify --list /boot/efi/EFI/UOS/shimx64.efi "
        ).read()
    elif "arm" in get_platform_arch():
        linuz_sig = os.popen(
            "echo 1|sudo -S cp /boot/vmlinuz-4.19.0-arm64-desktop /home/uos/vmlinuz.gz;echo 1|sudo -S gunzip ~/vmlinuz.gz ~/vmlinuz;echo 1|sudo -S sbverify --list ~/vmlinuz | grep 'Uniontech UEFI CA'"
        ).read()
        grub_sig = os.popen(
            "echo 1|sudo -S sbverify --list /boot/efi/EFI/UOS/grubaa64.efi | grep 'Uniontech UEFI CA'"
        ).read()
        shim_sig = os.popen(
            "echo 1|sudo -S sbverify --list /boot/efi/EFI/UOS/grubaa64.efi | grep 'Uniontech UEFI CA'"
        ).read()
        # 如下是debug信息，失败时候打印
        linuz_sig_debug = os.popen(
            "echo 1|sudo -S cp /boot/vmlinuz-4.19.0-arm64-desktop /home/uos/vmlinuz.gz;echo 1|sudo -S gunzip ~/vmlinuz.gz ~/vmlinz;echo 1|sudo -S sbverify --list ~/vmlinuz"
        ).read()
        grub_sig_debug = os.popen(
            "echo 1|sudo -S sbverify --list /boot/efi/EFI/UOS/grubaa64.efi"
        ).read()
        shim_sig_debug = os.popen(
            "echo 1|sudo -S sbverify --list /boot/efi/EFI/UOS/shimaa64.efi "
        ).read()
    else:
        pytest.mark.skip()
    logging.debug(f"内核签名信息如下:{linuz_sig_debug}")
    logging.debug(f"grub签名信息如下:{grub_sig_debug}")
    logging.debug(f"shim签名信息如下:{shim_sig_debug}")

    if linuz_sig != "" and grub_sig != "" and shim_sig != "":
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
