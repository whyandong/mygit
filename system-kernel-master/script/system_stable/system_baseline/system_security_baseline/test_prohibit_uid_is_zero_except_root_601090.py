#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:      601090
# @Test Description:  禁止存在除 `root` 之外 `UID` 为 `0` 的用户
# @Test Condition:
# @Test Step:         1.执行命令awk -F":" '{print $1 , $3}'  /etc/passwd | awk '{print $2}' | grep -w '0' | wc -l
# @Test command:
# @Test expect Result: 1.只有root的uid为0，命令返回为1
# @Test Remark:
# @Author:  杨浪_ut001228
# @Date: 2022/5/11
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


def test_prohibit_uid_is_zero_except_root_601090():
    logging.info("step1:执行命令")

    cmd1 = r"echo 1|sudo -S awk -F ':' '{print $1,$3}' /etc/passwd | awk '{print $2}'|grep -w '0'|wc -l"

    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    res1 = p001.stdout.read().replace("验证成功", "").replace("请输入密码",
                                                          '').strip(" \n")

    logging.info("禁止存在除 `root` 之外 `UID` 为 `0` 的用户返回值为:" + res1)

    if "1" in res1:
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        logging.error("step1:禁止存在除 `root` 之外 `UID` 为 `0` 的用户返回值错误,请检查！")
        assert False
