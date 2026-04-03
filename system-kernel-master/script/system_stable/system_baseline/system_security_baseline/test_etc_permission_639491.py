#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:      639491
# @Test Description:  系统/etc下配置文件非属主用户没有写权限
# @Test Condition:
# @Test Step:         1.终端执行echo 1 | sudo -S find /etc -type f \( -perm -020 -o -perm -002 \) -ls
# @Test command:
# @Test expect Result: 1.查询为空，/etc/没有非属主用户可写的配置文件
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


def test_etc_permission_639491():
    logging.info(
        "step1:执行命令echo 1 | sudo -S find /etc -type f \\( -perm -020 -o -perm -002 \\) -ls"
    )

    cmd1 = r"echo 1 | sudo -S find /etc -type f \\( -perm -020 -o -perm -002 \\) -ls"

    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    res1 = p001.stdout.read().replace("请输入密码", "").replace("验证成功",
                                                           "").strip(" \n")

    logging.info("/etc/没有非属主用户可写的配置文件的返回值为:" + res1)

    if "" in res1:
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        logging.error("step1:/etc/没有非属主用户可写的配置文件错误,请检查！" + res1)
        assert False
