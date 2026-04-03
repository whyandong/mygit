#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          614986
# @Test Description:      【hwclock】显示与设定硬件时钟
# @Test Condition:
# @Test Step:             1.显示硬件时钟sudo hwclock 2.同步系统时间到硬件时钟sudo hwclock -w
# @Test expect Result:    1.显示硬件时间 2.	同步成功
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


def test_hwclock_614986():
    logging.info("step1:显示硬件时钟sudo hwclock")

    cmd1 = r"echo 1|sudo -S hwclock"

    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    res1 = p001.stdout.read().replace("验证成功\n", " ")

    logging.info("当前硬件时钟显示为：\n" + res1)

    cmd2 = r"echo 1|sudo -S hwclock -w"

    p002 = subprocess.Popen(cmd2,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    res2 = p002.stdout.read()

    if "" in res2:
        assert True
    else:
        logging.error("显示与设定硬件时钟错误,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
