#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          625118
# @Test Description:      systemd-binfmt.service服务在local-fs.target之后启动
# @Test Condition:
# @Test Step:           1.检查systemd-binfmt服务配置 2.检查systemd-binfmt.service服务启动瀑布流
# @Test expect Result:  1.服务配置包含After=local-fs.target 2.systemd-binfmt.service服务启动瀑布流中包含local-fs.target
# @Test Remark:
# @Author:  夏曙_ut000220
# @Date:    2022/5/11
# *****************************************************
import sys
import pytest
import logging

from frame.common import execute_command
from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enable stage !")
    yield
    logging.info("this is env disable stage !")


def test_systemd_binfmt_service_625118():
    logging.info("step1:检查systemd-binmt.service服务配置是否包含After=local-fs.target")
    cmd1 = "systemctl cat systemd-binfmt.service 2>/dev/null | grep After=local-fs.target"
    res1 = execute_command(cmd1)
    logging.debug(res1)
    logging.info("step2:检查systemd-binfmt.service启动瀑布流是否包含local-fs.target")
    cmd2 = "systemd-analyze critical-chain systemd-binfmt.service | grep local-fs.target"
    res2 = execute_command(cmd2)
    logging.debug(res2)

    if res1 == "" or res2 == "":
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        logging.error("检查systemd-binmt.service服务配置失败，请检查！")
        logging.error(res2)
        assert False
    else:
        assert True
