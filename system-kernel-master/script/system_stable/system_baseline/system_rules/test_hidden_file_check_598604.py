#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:      598604
# @Test Description:  系统中不存在异常隐藏文件
# @Test Condition:
# @Test Step:
# 1.使用root用户，检查系统是否存在以..开头的隐藏文件
# 2.使用root用户，检查系统是否存在空格开头的隐藏文件
# @Test expect Result:
# 1.系统不存在以..开头的隐藏文件
# 2.系统不存在以空格开头的隐藏文件
# @Test Remark:
# @Author:  闫东_ut003274
# find / -name "..*" -print | cat -v
# find / -name " *" -print | cat -v
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


def test_hidden_file_check_598604():
    logging.info("step1:使用root用户, 检查系统是否存在以..开头的隐藏文件")
    cmd = r"echo 1|sudo -S find / -name '..*' -print 2>/dev/null"
    p001 = subprocess.Popen(cmd,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    res1 = p001.stdout.read().replace("验证成功", "").replace("请输入密码",
                                                          "").strip(" \n")
    step1 = "exec command: " + cmd + " return " + res1

    if res1 != "":
        logging.error(step1)
        ret1 = False
    else:
        logging.info(step1)
        ret1 = True

    logging.info("step2:使用root用户, 检查系统是否存在空格开头的隐藏文件")
    cmd = r"echo 1|sudo -S find / -name ' *' -print 2>/dev/null"
    p002 = subprocess.Popen(cmd,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    res2 = p002.stdout.read().replace("验证成功", "").replace("请输入密码",
                                                          "").strip("\n")
    if "/..deb" == res2:
        res2 = ""

    step2 = "exec command: " + cmd + " return " + res2
    if res2 != "":
        logging.error(step2)
        ret2 = False
    else:
        logging.info(step2)
        ret2 = True

    tsc_name = sys._getframe().f_code.co_name
    ret = ret1 and ret2

    if not ret:
        system_kernel_log_cap(tsc_name)
    assert ret
