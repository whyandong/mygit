#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          615494
# @Test Description:
# @Test Condition:
# @Test Step:            1.测试sfdisk是否正常执行
# @Test expect Result:   1.sfdisk正常执行
# @Test Remark:
# @Author:  夏曙_ut000220
# @Date: 2022/5/26
# *****************************************************

import sys
import pytest
import logging
import subprocess
from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_sfdisk_615494():
    logging.info("step1: 测试sfdisk是否正常执行")
    cmd1 = r"echo 1 | sudo -S sfdisk -l"
    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    fdisk_info = p001.stdout.read().replace("请输入密码", "").replace("验证成功",
                                                                 "").strip()

    if fdisk_info != "":
        assert True
    else:
        logging.error("sfdisk -l获取系统分区信息失败,请检查：")
        logging.debug(fdisk_info)
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
