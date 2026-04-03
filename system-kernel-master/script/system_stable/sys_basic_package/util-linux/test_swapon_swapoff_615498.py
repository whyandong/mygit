#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          615498
# @Test Description:
# @Test Condition:
# @Test Step:            1.查看初始交换分区大小 2.禁用交换分区后，检查交换分区大小 3.启用交换分区，检查交换分区大小
# @Test expect Result:   1.初始交换分区大小不为0 2.交换分区大小为0 3.交换分区大小不为0
# @Test Remark:
# @Author:  夏曙_ut000220
# @Date: 2022/5/27
# *****************************************************

import sys
import os
import pytest
import logging
import subprocess
from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_swapon_swapoff_615498():
    get_swap_total = r"free | grep Swap | awk '{print $2}'"
    get_swap_used = r"free | grep Swap | awk '{print $3}'"
    get_swap_device = r"blkid | grep swap | awk -F: '{print $1}'"

    logging.info("step1: 查看初始交换分区大小")
    p001 = subprocess.Popen(get_swap_total,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    swap_default_total = p001.stdout.read().replace("请输入密码",
                                                    "").replace("验证成功",
                                                                "").strip()
    p002 = subprocess.Popen(get_swap_used,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    swap_used_total = p002.stdout.read().replace("请输入密码",
                                                 "").replace("验证成功",
                                                             "").strip()
    p003 = subprocess.Popen(get_swap_device,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    swap_device = p003.stdout.read().replace("请输入密码",
                                             "").replace("验证成功",
                                                         "").strip("\n")
    logging.info("swap_device:" + swap_device)
    if int(swap_used_total) == 0:
        logging.info("step2: 禁用交换分区，查看交换分区大小")
        swapoff = r"echo 1|sudo -S swapoff " + swap_device
        os.system(swapoff)
        p004 = subprocess.Popen(get_swap_total,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding='utf-8')
        swap_off_total = p004.stdout.read().replace("请输入密码",
                                                    "").replace("验证成功",
                                                                "").strip("\n")
    else:
        pytest.skip("step2: 交换分区正常使用中...无法禁用，跳过此项测试")

    logging.info("step3: 启用交换分区，查看交换分区大小")
    swapon = r"echo 1 | sudo -S swapon " + swap_device
    os.system(swapon)
    p005 = subprocess.Popen(get_swap_total,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    swap_on_total = p005.stdout.read().replace("请输入密码",
                                               "").replace("验证成功", "").strip()
    logging.debug("swap_default_total:" + str(swap_default_total))
    logging.debug("swap_off_total:" + str(swap_off_total))
    logging.debug("swap_on_total:" + str(swap_on_total))
    if int(swap_default_total) != 0 and int(
            swap_off_total) == 0 and int(swap_on_total) != 0:
        assert True
    else:
        logging.error("交换分区启用和禁用失败，请检查：")
        logging.debug("swap_default_total: " + swap_default_total)
        logging.debug("swap_off_total: " + swap_off_total)
        logging.debug("swap_on_total: " + swap_on_total)
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
