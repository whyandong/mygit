#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:     639431
# @Test Description: 系统只有用户创建的账号和root账号具有登陆属性
# @Test Condition:
# @Test Step:          cat /etc/passwd | grep bash
# @Test expect Result: 只有root账号和用户安装创建的账号
'''返回结果包含
root:x:0:0:root:/root:/bin/bash
uos:x:1000:1000::/home/uos:/bin/bash
test:x:1002:1002::/home/test:/bin/bash
'''
# @Test Remark:
# @Author:  ut002037
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


def test_check_user_login_attr_check_639431():
    logging.info("step1 获取具有login属性的用户")
    cmd1 = "cat /etc/passwd | grep /bin/bash|awk -F ':' '{print $1}'"

    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    user_login_attr_lst = p001.stdout.read().replace("请输入密码", "").replace(
        "验证成功", "").split("\n")
    logging.debug(user_login_attr_lst)

    cmd2 = "cd /home;ls"
    p002 = subprocess.Popen(cmd2,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    acture_user_lst = p002.stdout.read().replace("请输入密码",
                                                 "").replace("验证成功",
                                                             "").split("\n")
    acture_user_lst.append("root")
    logging.debug(acture_user_lst)
    tmp = list(set(acture_user_lst) - set(user_login_attr_lst))
    tmp1 = list(set(user_login_attr_lst) - set(acture_user_lst))
    if len(tmp) == 0 and len(tmp1) == 0:
        assert True
    else:
        logging.error("实际有登陆属性的用户清单：" + user_login_attr_lst)
        logging.error("home目录下的用户清单:" + acture_user_lst)
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
