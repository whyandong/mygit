#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          656307
# @Test Description:      ssh超时配置检查
# @Test Condition:
# @Test Step:            1.ssh超时配置检查 /etc/profile /etc/ssh/sshd_config
# @Test expect Result:   1. ssh超时为900
# @Test Remark:
# @Author:  杨浪_ut001228
# @Date: 2022/4/14
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


@pytest.mark.skipif(int(get_system_version()) < 1050, reason="该用例只支持1050版本以上运行")
def test_ssh_tmout_check_656307():
    logging.info("step1:ssh超时配置检查 /etc/profile /etc/ssh/sshd_config")

    etc_profile_file = execute_command("cat /etc/profile | grep TMOUT")

    logging.info("/etc/profile配置文件为" + etc_profile_file)

    sshd_config = execute_command("cat /etc/ssh/sshd_config")

    logging.info("sshd_config配置文件为" + sshd_config)

    if "TMOUT=900" in etc_profile_file and "ClientAliveInterval 900" in sshd_config:
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        logging.error("step1:系统的ssh超时配置检查不正确,请检查！")
        assert False
