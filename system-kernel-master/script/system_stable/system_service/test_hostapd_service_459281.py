#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          459281<-----475228
# @Test Description:      检查hostapd是否预装，且是否被标记为masked状态
# @Test Condition:
# @Test Step:           1.检查hostapd是否已预装 2.检查hostapd服务状态
# @Test expect Result:  1.hostapd已经预装 2.hostapd服务为masked状态
# @Test Remark:
# @Author:  杨浪_ut001228
# *****************************************************
import sys
import pytest
import logging


from frame.common import execute_command
from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_hostapd_service_459281():
    logging.info("step1:检查hostapd是否已预装")

    cmd1 = "dpkg -l | grep hostapd |awk -F ' ' '{print $1}'"

    hostapd_check = execute_command(cmd1)

    if "ii" in hostapd_check:
        logging.info("step1:hostapd已预装!")
        assert True
    else:
        logging.error("step1:hostapd没有预装")
        assert False

    cmd1 = "systemctl status hostapd.service | grep Loaded |awk -F ':' '{print$2}' | awk -F ' ' '{print$1}'"

    tomcat_ser = (execute_command(cmd1)).split()

    logging.info("step2:检查服务状态是否为masked")

    if "masked" in tomcat_ser:
        assert True
    else:
        logging.error("服务状态不为masked,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
