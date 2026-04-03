#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:      601045
# @Test Description: 安全仓库地址检查
# @Test Condition:    all
# @Test Step:       cat /etc/apt/sources.list.d/security.list
# @Test expect:     安全仓库地址：deb https://professional-security.chinauos.com  eagle/xxx  main contrib non-free
#                   其中xxx为对应产品版本号，如eagle/1050、eagle/1060
# @Test Remark:
# @Author:  ut002037
# @Date:    2021/12/15
# *****************************************************
import sys
import logging
import pytest

from frame.common import execute_command, system_kernel_log_cap
from frame.common import get_system_version1


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_check_security_repository_601045():
    tsc_name = sys._getframe().f_code.co_name
    sys_version = get_system_version1()
    expect_src = 'deb https://professional-security.chinauos.com  eagle/' + sys_version + ' main contrib non-free'
    cmd = "cat /etc/apt/sources.list.d/security.list"

    acture_src = execute_command(cmd).strip("\n")
    logging.debug("执行cmd:" + cmd + "return:" + acture_src + " which expect:" +
                  expect_src)
    if acture_src in expect_src:
        assert True
    else:
        system_kernel_log_cap(tsc_name)
        logging.error("acture_src:" + acture_src)
        logging.error("expect_src:" + expect_src)
        assert False
