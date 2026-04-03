#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:      468377<--476652
# @Test Description:  密钥等文件的权限检查
# @Test Condition:
# @Test Step:
# step1:普通用户uos登录，执行ssh-keygen生成密钥,执行ls -al /home/uos/.ssh/id_rsa
# step2:执行sudo su切到root用户，执行ssh-keygen生成密钥,执行ls -al /root/.ssh/id_rsa
#
# @Test expect Result:
# 1 文件权限对应为0400, 只能被root账户读取
# 2 文件权限对应为0400, 只能被root账户读取
# @Test Remark:
# @Author:  郭斌_ut000253
# *****************************************************

import sys
import os
import pytest
import logging

from frame.common import execute_command
from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_ssh_key_check_468377():

    # 判断如果不存在密钥文件，普通用户生产密钥
    logging.info("step1: 检查/home/uos/.ssh/id_rsa权限")
    if not os.path.exists("/home/uos/.ssh/id_rsa"):
        logging.info("do ssh-keygen as uos")
        os.system("ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa >/dev/null 2>&1")
    # 查询普通获取目录权限
    usr_count = execute_command(
        "ls -l /home/uos/.ssh/id_rsa |cut -c1-10|tr \"rwx-\" \"4210\"|awk -F \"\" '{print $1+$2+$3$4+$5+$6$7+$8+$9}'"
    )
    logging.info(usr_count)
    logging.info("step2: 检查/root/.ssh/id_rsa权限")
    # 判断如果不存在密钥文件，切换root用户生产密钥
    # execute_command("echo '1'| sudo -S su") # 不需要切换到root用户，调用sudo生成密钥即可

    root_exist_rsa = os.system("echo 1 | sudo -S [ -f /root/.ssh/id_rsa ]")
    logging.info("root_exist_rsa: " + str(root_exist_rsa))
    if root_exist_rsa != 0:
        logging.info("do ssh-keygen as root")
        os.system(
            "echo 1 | sudo -S ssh-keygen -t rsa -P '' -f /root/.ssh/id_rsa >/dev/null 2>&1"
        )
    # 查询root获取目录权限
    root_count = execute_command(
        "echo '1'| sudo -S ls -l /root/.ssh/id_rsa |cut -c1-10|tr \"rwx-\" \"4210\"|awk -F \"\" '{print $1+$2+$3$4+$5+$6$7+$8+$9}'"
    )
    logging.info(root_count)

    # 判断查询结果，如果文件权限不等于400则断言错误
    if int(usr_count) == int(root_count) == 400:
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
