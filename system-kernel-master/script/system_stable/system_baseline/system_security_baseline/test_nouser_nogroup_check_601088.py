#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          601088
# @Test Description:      禁止存在无属组文件
# @Test Condition:
# @Test Step:            1.查看系统中是否存在无属主和属组的文件
# @echo 1|sudo -S find / ( -nouser -o -nogroup s) -ls
# @Test expect Result:   1.系统中不存在无属主和属组的文件
# @Test Remark:
# @Author:  杨浪_ut001228
# @Date: 2022/4/14
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


def test_usr_login_encrypt_601047():
    logging.info("step1:查看系统中是否存在无属主和属组的文件")
    cmd1 = "echo 1|sudo -S find / \\( -nouser -o -nogroup \\) -ls 2>/dev/null"
    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    res1 = p001.stdout.read().replace("验证成功", '').replace("请输入密码",
                                                          '').strip(" \n")
    step1 = "exec command: " + cmd1 + " return " + res1
    logging.debug(step1)

    if res1 == "":
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        logging.error("step1:系统中存在无属主和属组的文件,请检查！")
        assert False
