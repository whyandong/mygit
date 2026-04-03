#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:           343528<---482992
# @Test Description:       /etc/issue配置文件检查
# @Test Condition:
# @Test Step:              1.检查系统/etc/issue是否与配置是否一致
# @Test expect Result:     1./etc/issue与配置是否一致
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


def test_etc_issue_343528():
    etc_issue = r'UnionTech OS GNU/Linux 20 \n \l'

    logging.info("step2:检查系统/etc/issue是否与配置一致")
    cmd1 = "cat /etc/issue"
    actual_etc_issue = (execute_command(cmd1)).strip("\n")
    logging.info(actual_etc_issue)

    if actual_etc_issue == etc_issue:
        assert True
    else:
        logging.error("系统/etc/issue与配置不一致, 请检查! ")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
