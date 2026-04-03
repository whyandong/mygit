#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          614979
# @Test Description:      计算文件内容在内核中占用的page数
# @Test Condition:
# @Test Step:             1.查看/etc/passwd文件在内核page数，执行命令fincore /etc/passwd
# @Test expect Result:    2.返回占用page信息
# @Test Remark:
# @Author: 杨浪_ut001228
# Date: 2022/5/19
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


def test_fincore_614979():
    logging.info("step1:查看/etc/passwd文件在内核page数,执行命令fincore /etc/passwd")

    cmd1 = r"fincore /etc/passwd"

    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    res1 = p001.stdout.read().replace("验证成功\n", " ")

    logging.info("返回占用page信息为:\n" + res1)

    if "RES" in res1 and "PAGES" in res1 and "SIZE" in res1 and "FILE" in res1:
        assert True
    else:
        logging.error("计算文件内容在内核中占用的page数,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
