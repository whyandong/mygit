#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          614997
# @Test Description:
# @Test Condition:
# @Test Step:            1.测试lscpu是否正常执行 2.检查lscpu获取的信息是否有unknow，以及model name 、CPU MHZ 、cache等信息是否正常
# @Test expect Result:   1.lscpu正常执行 2.lscpu获取正常CPU信息正常，没有unknow， model name 、CPU MHZ 、cache等信息均正常
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


def test_lscpu_check_614994():
    logging.info("step1: 测试lscpu是否正常执行")
    cmd1 = r"lscpu"
    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    lscpu_info = p001.stdout.read().strip().split("\n")

    cmd2 = r"cat /proc/cpuinfo | grep 'model name' | head -n 1"
    p002 = subprocess.Popen(cmd2,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    cpuinfo_model_name = p002.stdout.read().split(":")[1].strip()

    unknow_info_lst = []
    mhz_info_lst = []
    cache_info_lst = []
    logging.info("step2: 检查lscpu获取的信息是否正常")
    for line in lscpu_info:
        if "unknow" in line:
            unknow_info_lst.append(line)
        if "Model name" in line:
            model_name_value = line.split(":")[1].strip()
        if "MHz" in line:
            mhz_info_value = line.split(":")[1].strip()
            mhz_info_lst.append(mhz_info_value)
        if "cache" in line:
            cache_info_value = line.split(":")[1].strip()
            cache_info_lst.append(cache_info_value)
    # unknow_info_lst.append("")
    if len(
            unknow_info_lst
    ) == 0 and model_name_value == cpuinfo_model_name and '0' not in mhz_info_lst and '0' not in cache_info_lst and "" not in mhz_info_lst and "" not in cache_info_lst:
        assert True
    else:
        logging.error(
            "lscpu信息检查失败,请检查是否有unknow信息,model name 、CPU MHZ 、cache是否有0或空值")
        logging.debug(unknow_info_lst)
        logging.debug(cpuinfo_model_name)
        logging.debug(model_name_value)
        logging.debug(mhz_info_lst)
        logging.debug(cache_info_lst)
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
