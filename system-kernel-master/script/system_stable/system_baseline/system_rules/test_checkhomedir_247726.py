#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          247726<---303400
# @Test Description:      /home目录规范性检查
# @Test Condition:
# @Test Step:           1.cd /home，执行ls
# @Test expect Result:  新装系统home目录下有且只有一个目录文件
# @Test Remark:
# @Author:  ut002037
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


def test_checkhomedir_247726():
    cmd1 = r'cd /home; ls'
    # cmd2 = r"cat /etc/passwd | grep 1000 | awk -F ':' '{print $1}'"

    home_dir = execute_command(cmd1).split()
    step1 = "step1 exec " + cmd1 + " return :"

    current_users = execute_command("whoami").strip(" \n")

    if len(home_dir) != 1 and current_users in home_dir:
        logging.error(step1)
        logging.error(home_dir)
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
    else:
        logging.info(step1)
        logging.info(home_dir)
        assert True
