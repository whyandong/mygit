#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          615500
# @Test Description:
# @Test Condition:
# @Test Step:            1.查看swaplabel修改swap分区标签和UUID 2.修改swap分区标签 3.再次查看swap分区标签和uuid
# @Test expect Result:   1.正常查看swap分区uuid和标签 2.修改成功 3.swap分区标签修改成功，uuid不变
# @Test Remark:
# @Author:  夏曙_ut000220
# @Date: 2022/5/30
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
    get_swap_dev = r"swapon | sed -n '2p' | awk '{print $1}'"
    p001 = subprocess.Popen(get_swap_dev,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    swap_device = p001.stdout.read().replace("请输入密码", "").replace("验证成功",
                                                                  "").strip()
    change_swap_label = r"echo 1 | sudo -S swaplabel -L SWAP " + swap_device
    os.system(change_swap_label)
    logging.info("this is env disable stage !")


def test_swaplabel_615500():
    get_swap_dev = r"swapon | sed -n '2p' | awk '{print $1}'"
    p001 = subprocess.Popen(get_swap_dev,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    swap_device = p001.stdout.read().replace("请输入密码", "").replace("验证成功",
                                                                  "").strip()
    logging.info("swap_device:" + swap_device)

    logging.info("step1: 查看swaplabel修改swap分区标签和UUID")
    get_swap_info = r"echo 1 | sudo -S swaplabel " + swap_device + "| awk '{print $2}'"
    p002 = subprocess.Popen(get_swap_info,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    swap_info_default = p002.stdout.read().replace("请输入密码", "").replace(
        "验证成功", "").strip().split("\n")
    logging.info(swap_info_default)
    uuid_default = swap_info_default[1]

    logging.info("step2: 修改swap分区标签")
    change_swap_label = r"echo 1 | sudo -S swaplabel -L SWAP1 " + swap_device
    os.system(change_swap_label)

    logging.info("step3: 再次查看swap分区标签和uuid")
    p003 = subprocess.Popen(get_swap_info,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    swap_info_2 = p003.stdout.read().replace("请输入密码", "").replace(
        "验证成功", "").strip().split("\n")
    logging.info(swap_info_2)
    label_2 = swap_info_2[0]
    uuid_2 = swap_info_2[1]

    if label_2 == "SWAP1" and uuid_2 == uuid_default:
        assert True
    else:
        logging.error("修改swap分区标签失败，请检查：")
        logging.debug("label_2:" + label_2)
        logging.debug("uuid_2:" + uuid_2)
        logging.debug("uuid_default:" + uuid_default)
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
