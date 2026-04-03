#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:      160880
# @Test Description:    仓库授权管理配置文件域名列表检查，确保所有仓库地址都有授权管理配置
# @Test Condition:    all
# @Test Step:       仓库授权管理配置文件域名列表检查
# @Test expect： 参考uniontest/configs/系统基线规范.xlsx
# @Test Remark:
# @Author:  ut000220
# @Date:    2022/5/19
# *****************************************************

import logging
import sys
import pytest
import subprocess

from frame.common import open_excel_file
from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_apt_auth_check_160880():
    # 打开待操作的sheet表单
    expect_apt_auth_lst = []
    apt_auth_lst = []
    sheet_op = open_excel_file("./configs/系统基线规范.xlsx", "apt_auth")
    max_row = sheet_op.max_row
    for row in range(2, max_row + 1):
        apt_auth_domain = sheet_op.cell(row=row, column=1).value.strip()
        expect_apt_auth_lst.append(apt_auth_domain)

    logging.info("step1: 获取仓库授权管理配置域名列表基线数据：")
    logging.debug(expect_apt_auth_lst)

    logging.info("step2:获取本机仓库授权管理配置域名列表：")
    cmd1 = r"cat /etc/apt/auth.conf.d/uos.conf | awk '{print $2}'"
    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    apt_auth_lst = p001.stdout.read().strip().split("\n")
    logging.debug(apt_auth_lst)

    # print(sys_port_list)
    # print(expect_port_lst)
    # print(expect_random_port)

    apt_auth_err = list(set(expect_apt_auth_lst) - set(apt_auth_lst))

    if len(apt_auth_err) == 0:
        assert True
    else:
        logging.error("存在未被授权的仓库:")
        for s in apt_auth_err:
            logging.error(s)
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
