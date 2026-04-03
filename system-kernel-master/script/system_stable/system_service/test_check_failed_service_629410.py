#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
# ****************************************************
# @Test Case ID:          629410
# @Test Description:      检查系统服务是否有启动failed
# @Test Condition:
# @Test Step:           1.检查系统服务是否有启动failed项
# @Test expect Result:  1.没有启动failed项
# @Test Remark:
# @Author:  夏曙_ut000220
# @Date:    2021/12/24
# *****************************************************
import sys
import pytest
from frame.common import execute_command, system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enable stage !")
    yield
    logging.info("this is env disable stage !")


def test_check_failed_service_629410():
    skip_service_lst = [
        "nvidia-persistenced.service", "x11vnc.service", "uos-reporter.service"
    ]
    cmd1 = "systemctl list-units --all --failed | grep 'loaded units listed' | awk '{print $1}'"
    cmd2 = "systemctl list-units --all --failed"
    service_failed_num = execute_command(cmd1).replace("\n", "")
    service_failed_log = execute_command(cmd2)
    for skip_service in skip_service_lst:
        if skip_service in service_failed_log:
            service_failed_num = int(service_failed_num) - 1

    logging.info(f"service_failed_num:{service_failed_num}")
    logging.info("step1:检查系统当前所有服务是否有启动failed项")
    if int(service_failed_num) == 0:
        assert True
    else:
        logging.error("-------系统服务有启动failed项--------\n" + service_failed_log)
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
