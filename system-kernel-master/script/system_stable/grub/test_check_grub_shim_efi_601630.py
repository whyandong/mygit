#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:           601630
# @Test Description:        检查boot目录下的grub.efi和shim.efi文件是否一致
# @Test Condition:
# @Test Step:              1.检查grub启动配置文件是否一致
# @Test expect Result:     1.grub启动配置文件一致
# @Test Remark:
# @Author:  夏曙_ut000220
# *****************************************************
import sys
import pytest
import logging
import os
from frame.common import system_kernel_log_cap
from frame.common import get_platform_arch


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_check_grub_shim_601630():
    sys_arch = get_platform_arch()
    if "amd" in sys_arch:
        grub1_md5 = os.popen(
            "echo 1|sudo -S md5sum /boot/efi/EFI/UOS/grubx64.efi").read(
            ).split()
        grub2_md5 = os.popen(
            "echo 1|sudo -S md5sum /boot/efi/EFI/Ubuntu/grubx64.efi").read(
            ).split()
        grub3_md5 = os.popen(
            "echo 1|sudo -S md5sum /boot/efi/EFI/boot/grubx64.efi").read(
            ).split()
        shim1_md5 = os.popen(
            "echo 1|sudo -S md5sum /boot/efi/EFI/UOS/shimx64.efi").read(
            ).split()
        shim2_md5 = os.popen(
            "echo 1|sudo -S md5sum /boot/efi/EFI/Ubuntu/shimx64.efi").read(
            ).split()
        shim3_md5 = os.popen(
            "echo 1|sudo -S md5sum /boot/efi/EFI/boot/shimx64.efi").read(
            ).split()
    elif "arm" in sys_arch:
        grub1_md5 = os.popen(
            "echo 1|sudo -S md5sum /boot/efi/EFI/UOS/grubaa64.efi").read(
            ).split()
        grub2_md5 = os.popen(
            "echo 1|sudo -S md5sum /boot/efi/EFI/Ubuntu/grubaa64.efi").read(
            ).split()
        grub3_md5 = os.popen(
            "echo 1|sudo -S md5sum /boot/efi/EFI/boot/grubaa64.efi").read(
            ).split()
        shim1_md5 = os.popen(
            "echo 1|sudo -S md5sum /boot/efi/EFI/UOS/shimaa64.efi").read(
            ).split()
        shim2_md5 = os.popen(
            "echo 1|sudo -S md5sum /boot/efi/EFI/Ubuntu/shimaa64.efi").read(
            ).split()
        shim3_md5 = os.popen(
            "echo 1|sudo -S md5sum /boot/efi/EFI/boot/shimaa64.efi").read(
            ).split()
    else:
        pytest.mark.skip()

    logging.info("step: 检查系统grub.efi和shim.efi文件是否一致：")
    logging.debug(grub1_md5)
    logging.debug(grub2_md5)
    logging.debug(grub3_md5)
    logging.debug(shim1_md5)
    logging.debug(shim2_md5)
    logging.debug(shim3_md5)
    if grub1_md5[0] == grub2_md5[0] == grub3_md5[0] and shim1_md5[
            0] == shim2_md5[0] == shim3_md5[0]:
        assert True
    else:
        logging.error("grub.efi或者shim.efi的md5不一致,请检查debug信息")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
