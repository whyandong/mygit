#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:      468158
# @Test Description:  /etc/shadow的文件权限检查查
# @Test Condition:
# @Test Step:
# 1.检查/etc/shadow文件权限
# ls -l /etc/shadow
# @Test expect Result:
# 文件权限对应为0640, 用户是root, 组是shadow
# @Test Remark:
# @Author:  ut003395--->郭斌_ut000253
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


def test_check_etc_shadow_468158():
    list2 = ['root']
    list3 = ['shadow']
    logging.info("查询 /etc/shadow 文件的权限")
    cmd1 = r"ls -l /etc/shadow |cut -c1-10|tr 'rwx-' '4210'|awk -F '' '{print $1+$2+$3$4+$5+$6$7+$8+$9}'"
    def_timer = int(execute_command(cmd1))
    logging.info(def_timer)

    logging.info("查询 /etc/shadow 文件的属主")
    cmd2 = "ls -l /etc/shadow | awk '{print $3}'"
    def2_timer = (execute_command(cmd2)).split()
    logging.info(def2_timer)

    logging.info("查询 /etc/shadow 文件的所属组")
    cmd3 = "ls -l /etc/shadow | awk '{print $4}'"
    def3_timer = (execute_command(cmd3)).split()
    logging.info(def3_timer)

    if def_timer == 640 and def2_timer == list2 and def3_timer == list3:
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
