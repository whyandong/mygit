#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          614977
# @Test Description:      创建指定大小的文件
# @Test Condition:
# @Test Step:             1.打开终端，执行fallocate -l 1g bigfile.txt
# @Test expect Result:    2.有文件bigfile.txt生成，大小为1G
# @Test Remark:
# @Author: 杨浪_ut001228
# Date: 2022/5/19
# *****************************************************
import sys
import os
import pytest
import logging
import subprocess

from frame.common import execute_command
from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    execute_command("rm -r bigfile.txt")
    logging.info("this is env disable stage !")


def test_fallocate_614977():
    logging.info("step1:打开终端,执行fallocate -l 1g bigfile.txt")

    cmd1 = r"fallocate -l 1g bigfile.txt"
    os.system(cmd1)

    cmd2 = r"ls -l|grep bigfile.txt"

    p002 = subprocess.Popen(cmd2,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    res2 = p002.stdout.read().replace("验证成功\n", " ")

    logging.info("生成文件为:" + res2)

    if "bigfile" in res2:
        assert True
    else:
        logging.error("创建指定大小的文件错误,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
