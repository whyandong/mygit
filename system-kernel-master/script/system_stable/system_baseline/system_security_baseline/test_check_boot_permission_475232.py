#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:      475232
# @Test Description:  /boot目录权限的检查
# @Test Condition:
# @Test Step:
# 1.查看/boot目录权限
# cd
# /ls -l | grep boot件
# @Test expect Result:
# 1./boot对应的权限为0700，属主为root
# @Test Remark:
# @Author:  闫东_ut003395
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


def test_check_boot_permission_475232():
    cmd = ''
    step = "exec " + cmd + " return:"
    logging.info("step1:查看/boot的权限")
    cmd = "ls -l / | grep boot|awk NR==1|cut -c1-10|tr 'drwx' '0421'|awk -F '' '{print $1$2+$3+$4$5+$6+$7$8+$9+$10}'"
    dir_mode = execute_command(cmd).rstrip()
    logging.info(str(step) + dir_mode)

    cmd = "ls -l / | grep boot |awk NR==1 | awk '{print $3}'"
    dir_owner = (execute_command(cmd)).rstrip()
    logging.info(str(step) + dir_owner)
    logging.info("check:/boot对应的权限为0700, 属主为root")

    ret = (dir_mode == '0700' and dir_owner == 'root')

    if not ret:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
    assert ret
