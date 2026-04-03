#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          614063
# @Test Description:      【blkid】基本功能测试
# @Test Condition:
# @Test Step:             1.打开终端，执行命令blkid
# @Test expect Result:    2.返回设置属性值
# @Test Remark:
# @Author: 杨浪_ut001228
# Date: 2022/5/17
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


def test_blkid_614063():
    logging.info("step1:打开终端,执行命令blkid")

    cmd1 = r"blkid"

    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    res1 = p001.stdout.read().replace("验证成功\n", " ")

    logging.info("blkid返回值为:\n" + res1)

    if "EFI" in res1 and "Boot" in res1 and "Roota" in res1 and "Rootb" in res1 and "_dde_data" in res1 and "Backup" in res1 and "SWAP" in res1:
        assert True
    else:
        logging.error("blkid返回值错误,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
