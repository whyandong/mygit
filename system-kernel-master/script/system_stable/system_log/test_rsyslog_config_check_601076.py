#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ****************************************************
# @Test Case ID:          601076
# @Test Description:      系统日志默认保存6个月，可配置保存时长与大小
# @Test Condition:
# @Test Step:             1.打开终端，执行命令sudo cat /etc/logrotate.d/rsyslog
# @Test expect Result:    1.返回结果中包含rotate 6 monthly
# @Test Remark:
# @Author: 杨浪_ut001228
# Date: 2022/5/20
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


def test_rsyslog_config_check_601076():
    logging.info("step1:打开终端，执行命令sudo cat /etc/logrotate.d/rsyslog")

    cmd1 = r"echo 1|sudo -S cat /etc/logrotate.d/rsyslog"

    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    res1 = p001.stdout.read().replace("验证成功\n", " ")
    logging.info("返回结果为:" + res1)

    if "rotate 6" in res1 and "monthly" in res1:
        assert True
    else:
        logging.error("系统日志默认配置错误,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
