#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          583238
# @Test Description:
# @Test Condition:
# @Test Step:            1.创建测试文件和针对文件的审计规则 2.对审计文件进行cat操作 3.过滤日志中对文件进行操作的审计日志
# @Test expect Result:   3.审计日志中可以查到针对审计文件的cat操作记录
# @Test Remark:
# @Author:  夏曙_ut000220
# @Date: 2022/5/19
# *****************************************************
import sys
import os
import pytest
import logging
import subprocess
from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    os.system("echo 1 | sudo -S systemctl restart auditd.service")
    yield
    os.system("echo 1 | sudo -S systemctl stop auditd.service")
    os.system("echo 1 | sudo -S rm /var/log/audit/audit.log")
    os.system("rm -rf ~/file.txt")
    logging.info("this is env disable stage !")


def test_auditd_583238():
    logging.info("step1: 创建测试文件和针对文件的审计规则")
    # create test file
    os.system('touch ~/file.txt')
    # 创建审计规则
    os.system("echo 1 | sudo -S auditctl -w ~/file.txt -p rwxa")

    logging.info("step2: 对审计文件进行cat操作")
    # 对审计文件进行操作，这里执行读操作
    os.system("cat ~/file.txt")

    # 获取审计日志
    logging.info("step3: 过滤日志中对文件进行操作的审计日志")
    cmd1 = r"echo 1 | sudo -S grep '/home/uos/file.txt' /var/log/audit/audit.log"
    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    path_msg = p001.stdout.read().replace("请输入密码", "").replace("验证成功",
                                                               "").split(' ')
    logging.info(path_msg)
    logging.info("step2: 过滤日志中对文件进行操作的审计日志")
    cmd2 = r"echo 1 | sudo -S grep '/usr/bin/cat' /var/log/audit/audit.log"
    p001 = subprocess.Popen(cmd2,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    syscall_msg = p001.stdout.read().replace("请输入密码",
                                             "").replace("验证成功", "").split(' ')
    logging.info(syscall_msg)
    if path_msg[1] == syscall_msg[1]:
        assert True
    else:
        logging.error("没有查询到对应的审计日志，请排查确认！")
        logging.debug(path_msg)
        logging.debug(syscall_msg)
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
