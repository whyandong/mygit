#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          614987
# @Test Description:      【ionice】显示/修改进程的IO调度与优先级
# @Test Condition:
# @Test Step:             1.查看进程的IO调度与优先级属性ionice  -p PID 2.修改进程的IO调度与优先级属性sudo ionice -c 2 -n 4 -p PID
# @Test Step:             3.查看进程的IO调度与优先级属性ionice  -p PID
# @Test expect Result:
# @Test Remark:
# @Author: 杨浪_ut001228
# Date: 2022/5/19
# *****************************************************
import os
import sys
import pytest
import logging
import subprocess

from frame.common import system_kernel_log_cap

ori_io_class = ""
ori_prio = 0


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def pharse_current_nice_prio(res):
    tmp = res.split(":")
    logging.debug(tmp[0] + tmp[1])
    if tmp[0] == "none":
        io_class = 0
    elif tmp[0] == "best-effort":
        io_class = 2
    elif tmp[0] == "real time":
        io_class = 3
    elif tmp[0] == "idle":
        io_class = 4
    prio = int(tmp[1].replace("prio", " ").strip(""))
    return (io_class, prio)


def test_ionice_614987():
    logging.info("step1:查看进程的IO调度与优先级属性ionice ")
    cmd1 = r"echo 1|sudo -S ionice  -p 1"
    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    res1 = p001.stdout.read().replace("验证成功\n", " ")
    logging.info("当前进程ionice值为:" + res1)
    tmp = pharse_current_nice_prio(res1)
    ori_io_class = tmp[0]
    ori_prio = tmp[1]
    logging.info("修改进程的IO调度与优先级属性")
    cmd2 = r"echo 1|sudo -S ionice -c 2 -n 4 -p 1"
    os.system(cmd2)

    cmd3 = r"echo 1|sudo -S ionice -p 1"
    p003 = subprocess.Popen(cmd3,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    res3 = p003.stdout.read().replace("验证成功\n", " ")
    logging.info("修改后进程ionice值为:" + res3)

    cmd = "echo 1|sudo -S ionice -c " + str(ori_io_class) + " -n " + str(
        ori_prio) + " -p 1"
    logging.info(cmd)
    os.system(cmd)
    if "4" in res3:
        assert True
    else:
        logging.error("显示/修改进程的IO调度与优先级错误,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
