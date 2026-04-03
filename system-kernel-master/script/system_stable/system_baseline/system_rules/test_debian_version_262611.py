#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:           262611<---262612
# @Test Description:       debian_version版本号检查
# @Test Condition:
# @Test Step:              1.debian_version版本号检查
# @Test expect Result:     1.debian_version版本号与debian源一致
# @Test Remark:
# @Author:  杨浪_ut001228
# *****************************************************
import sys
import pytest
import logging


from frame.common import execute_command
from frame.common import system_kernel_log_cap
from frame.common import get_system_version


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_debian_version_262611():
    logging.info("系统版本大于1040, 继续执行用例! ")

    logging.info("step1:检查系统备份还原依赖是否与配置一致")

    cmd1 = "cat /etc/debian_version"

    debian_version = execute_command(cmd1).split()

    logging.info(debian_version)

    list1 = ['10.10']

    if debian_version == list1:
        assert True
    else:
        logging.error("debian_version版本与源版本不一致,请检查!")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
