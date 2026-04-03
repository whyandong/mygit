#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          614985
# @Test Description:      【hexdump】不同格式下文件显示
# @Test Condition:
# @Test Step:
# 1.按照指定格式显示文件内容
# hexdump - b 1.txt
# hexdump - c 1.txt
# hexdump - C 1.txt
# hexdump - d 1.txt
# @Test expect Result:
# 1.返回占相应格式信息
# @Test Remark:
# @Author: 杨浪_ut001228
# Date: 2022/5/19
# *****************************************************
import sys
import os
import pytest
import logging
import subprocess

from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    os.system("echo 1234 >1.txt")
    yield
    os.system("rm 1.txt")


def test_hexdump_614985():
    logging.info("step1:按照指定格式显示文件内容")
    cmd1 = r"hexdump -b 1.txt"
    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    res1 = p001.stdout.read().replace("验证成功\n", " ")
    logging.info("八进制显示文件内容为:" + res1)

    cmd2 = r"hexdump -c 1.txt"
    p002 = subprocess.Popen(cmd2,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    res2 = p002.stdout.read().replace("验证成功\n", " ")
    logging.info("单字节显示文件内容为:" + res2)

    cmd3 = r"hexdump -C 1.txt"
    p003 = subprocess.Popen(cmd3,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    res3 = p003.stdout.read().replace("验证成功\n", " ")
    logging.info("标准的hex+asccii格式显示文件内容为:" + res3)

    cmd4 = r"hexdump -d 1.txt"
    p004 = subprocess.Popen(cmd4,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    res4 = p004.stdout.read().replace("验证成功\n", " ")
    logging.info("两byte十进制格式显示文件内容为:" + res4)

    if "0000000 061 062" in res1 and "0000000   1   2   3 " in res2 and "00000000  31 32 " in res3 and "0000000   12849" in res4:
        assert True
    else:
        logging.error("不同格式下文件显示错误,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
