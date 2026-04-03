#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import pytest
import logging
from frame.common import execute_command
from frame.common import system_kernel_log_cap

# ****************************************************
# @Test Case ID:    598630
# @Test Description:目录访问控制-禁止用户间家目录可互相访问
# @Test Condition:  新建帐号test，test1
# @Test Step:
'''
# 1 登录test帐号,访问/home/test1目录
# 2 登录test1账户,访问/home/test目录
# 3 检查/etc/login.defs文件UMASK的值
    cat /etc/login.defs | grep "UMASK"
'''
# @Test expect Result:
'''
# 1 test1账户目录为锁定状态,双击提示没有查看权限
# 2 test账户目录为锁定状态,双击提示没有查看权限
# 3 由原来的022更新成027
'''

# @Test Remark:
# @Author:  ut002037
# *****************************************************


def user_add(username):
    cmd = "echo 1|sudo -S useradd " + username + " -m -s /bin/bash"
    ret = os.system(cmd)
    if ret == 0:
        logging.info("新增用户" + username + " succeed !")


def get_current_username():
    username = execute_command("whoami").strip("\n").replace("请输入密码",
                                                             "").replace(
                                                                 "验证成功", "")
    logging.info("current user is :" + username)
    return username


def delete_pwd(username):
    cmd = "echo 1|sudo -S passwd -d " + username
    if os.system(cmd) == 0:
        logging.info("禁用账户" + username + "密码succeed!")


def delete_user(username):
    cmd = "echo 1|sudo -S userdel -r " + username + " 2>/dev/null"
    ret = os.system(cmd)
    if ret == 0:
        logging.info("delete user:" + username + " succeed!")


def access_userdir(username, userdir):
    cmd = "sudo -u " + username + " ls -l " + userdir
    ret = execute_command(cmd)
    logging.debug(ret)
    if "权限不够" in ret:
        return 0
    else:
        return 1


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    # logging.info("创建测试用户test1!")
    user_add("test1")
    user_add("test2")
    delete_pwd("test1")
    delete_pwd("test2")
    yield
    delete_user("test1")
    delete_user("test2")
    # logging.info("删除测试用户test1!")


def test_home_dir_access_ctrl_598630():
    ret1 = access_userdir("test1", "/home/test2")
    logging.debug(str(ret1))

    ret2 = access_userdir("test2", "/home/test1")
    logging.debug(str(ret2))

    cmd = "cat /etc/login.defs|grep 'UMASK'"
    ret = execute_command(cmd)
    if "027" in ret:
        ret3 = 0
    else:
        ret3 = 1
    ret = ret1 + ret2 + ret3
    if ret == 0:
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
