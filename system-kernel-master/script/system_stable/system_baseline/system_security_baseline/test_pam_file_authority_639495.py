#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          639495
# @Test Description:      检查pam鉴权配置文件默认权限
# @Test Condition:
# @Test Step:            1.检查pam鉴权配置文件默认权限
# @Test expect Result:   1.默认权限644
# @Test Remark:
# @Author:  杨浪_ut001228
# @Date: 2022/4/14
# *****************************************************
import sys
import pytest
import logging
import subprocess

from frame.common import system_kernel_log_cap, parse_file_perssion


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_pam_file_authority_639495():
    logging.info("step1:检查pam鉴权配置文件默认权限")

    cmd1 = "ls -al /etc/pam.d/common-auth |awk '{print $1}'"

    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    res1 = p001.stdout.read().strip(" \n")

    logging.info("pam鉴权配置文件默认权限为:" + res1)
    perm = parse_file_perssion(res1)

    if perm == "644":
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        logging.error("step1:pam鉴权配置文件默认权限不为644,请检查！")
        assert False
