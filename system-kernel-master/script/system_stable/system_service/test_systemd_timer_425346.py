#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          425346
# @Test Description:      系统自启动timer检查
# @Test Condition:
# @Test Step:           1.查询系统自启动timer与基线对比是否一致
# @Test expect Result:  1.与基线一致
# @Test Remark:
# @Author:  夏曙_ut000220
# @Date:    2021/12/22
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


def test_systemd_timer_425346():
    logging.info("step1:查询系统自启动timer与基线对比是否一致")

    cmd1 = "systemctl list-unit-files | grep timer | grep enabled | awk '{print $1}'"

    timer_enabled_base = ["apt-daily-upgrade.timer", "apt-daily.timer",
                          "laptop-mode.timer", "logrotate.timer", "man-db.timer"]

    timer_enabled_list = (execute_command(cmd1)).split()

    if timer_enabled_list.sort() == timer_enabled_base.sort():
        assert True
    else:
        logging.error("查询系统自启动timer与基线对比不一致,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
