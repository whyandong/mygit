#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ****************************************************
# @Test Case ID:          649236
# @Test Description:      ul命令测试
# @Test Condition:
# @Test Step:             1.创建测试文件：echo -e 'h\b_e\b_l\b_l\b_o\b_ word'  > testfile.txt 2.执行ul testfile.txt
# @Test expect Result:    2.打印hello word ( hello有下划线）
# @Test Remark:
# @Author: 杨浪_ut001228
# Date: 2022/5/20
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
    os.system("rm -r testfile.txt")
    logging.info("this is env disable stage !")


def test_ul_649236():
    logging.info("step1:创建测试文件：")
    cmd1 = r"echo  -e  'h\b_e\b_l\b_l\b_o\b_ word' >testfile.txt"
    os.system(cmd1)

    cmd2 = r"ul testfile.txt"
    p002 = subprocess.Popen(cmd2,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    res2 = p002.stdout.read().replace("验证成功\n", " ")
    logging.info("打印测试文件内容:" + res2)

    if "word" in res2:
        assert True
    else:
        logging.error("ul命令错误,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
