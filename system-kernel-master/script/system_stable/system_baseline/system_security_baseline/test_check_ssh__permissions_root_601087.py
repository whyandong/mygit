#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:      601087
# @Test Description: 禁止root用户ssh
# @Test Condition:    all
# @Test Step:       查看ssh的配置文件，cat /etc/ssh/sshd_config | grep PermitRootLogin，查看PermitRootLogin是否注释
# @Test expect:     PermitRootLogin是注释
# @Test Remark:
# @Author:  ut003274
# @Date:    2021/12/15
# *****************************************************
import sys
import logging
import pytest

from frame.common import root_exec_cmd, system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_check_ssh__permissions_root_601087():
    tsc_name = sys._getframe().f_code.co_name
    cmd_dict = {
        # 执行命令：["预期返回结果"]
        "cat /etc/ssh/sshd_config | grep PermitRootLogin | sed -n '1p' ":
        ['#PermitRootLogin prohibit-password']
    }
    err_count = 0
    for cmd, expect_res in cmd_dict.items():
        res, step = root_exec_cmd(cmd, expect_res, tsc_name)
        if res < len(expect_res):
            logging.info(step)
        else:
            logging.error(step)
            err_count += 1
    if err_count == 0:
        assert True
    elif err_count > 0:
        system_kernel_log_cap(tsc_name)
        assert False
