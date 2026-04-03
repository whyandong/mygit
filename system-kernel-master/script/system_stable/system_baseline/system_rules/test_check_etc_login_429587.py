#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:      429587<---343561
# @Test Description:  /etc/login.defs配置文件检查
# @Test Condition:    加仓库安装login包测试的情况下，安装过程中提示“保留原/etc/login.defs配置”选择Y
# @Test Step:
# 1.执行cat /etc/login.defs检查配置文件
#
# @Test expect Result:
# 1.配置文件有如下参数：
# SUB_UID_MAX  1000000000
# SUB_GID_MAX  1000000000
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
    # execute_command("echo '1'| sudo -S apt install login")
    yield
    # execute_command("echo '1'| sudo -S apt remove login")


def test_check_etc_login_429587():
    list1 = ['SUB_GID_MAX', '1000000000']
    list2 = ['SUB_UID_MAX', '1000000000']
    logging.info("step1:检查/etc/login.defs配置文件")
    cmd1 = "cat /etc/login.defs | grep 'SUB_GID_MAX'"
    gid = execute_command(cmd1).split()
    cmd2 = "cat /etc/login.defs | grep 'SUB_UID_MAX'"
    uid = execute_command(cmd2).split()

    if gid == list1 and uid == list2:
        assert True
    else:
        logging.error(" /etc/login.defs配置错误, 请检查! ")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
