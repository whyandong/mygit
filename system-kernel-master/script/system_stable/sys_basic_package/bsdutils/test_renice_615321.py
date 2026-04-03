#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          615321
# @Test Description:      【renice】改变进程的优先级
# @Test Condition:
# @Test Step:             1.修改进程的nice值，执行命令 sudo renice -n 5 -p "PID"  -u root 2.获取进程修改后的nice值，执行命令：ps -elf | grep "PID"
# @Test expect Result:    1.正常修改进程renice值  2.修改后的进程renice值为5
# @Test Remark:
# @Author: 杨浪_ut001228
# Date: 2022/5/19
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


def test_renice_615321():
    logging.info("step1:修改进程的nice值")

    cmd1 = r"echo 1|sudo -S renice -n 5 -p 1 -u root"
    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    res1 = p001.stdout.read().replace("验证成功\n", " ")
    logging.info("修改进程的nice值为:" + res1)

    logging.info("查看修改后的进程renice值")

    cmd2 = r"echo 1|sudo -S ps -elf | grep 1|awk -F ' ' '{print $8}'|awk 'NR==2'"

    p002 = subprocess.Popen(cmd2,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    res2 = p002.stdout.read().replace("验证成功\n", " ")
    logging.info("修改后进程的nice值为:" + res2)

    if "5" in res2:
        assert True
    else:
        logging.error("修改后的进程renice错误,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
