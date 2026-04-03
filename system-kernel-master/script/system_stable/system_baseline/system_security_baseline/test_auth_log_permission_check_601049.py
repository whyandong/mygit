#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:    601049
# @Test Description: auth.log需要鉴权才能查看
# @Test Condition:
# @Test Step:   1.查看auth.log文件权限 2.检查管理员用户组是否包含adm 3.普通用户读取auth.log文件 4.普通用户sudo提权后读取auth.log文件
# @Test command:
# @Test expect Result:   1.系统中不存在无属主和属组的文件
# @Test Remark:
# @Author:  夏曙_ut000220
# @Date: 2022/5/24
# *****************************************************
import sys
import pytest
import logging
import subprocess

from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enable stage !")
    yield
    logging.info("this is env disable stage !")


def test_auth_log_permission_check_601049():
    logging.info("step1:查看auth.log文件权限是否是640")
    cmd1 = r"ls -la /var/log/auth.log | awk '{print $1,$3,$4}'"
    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    auth_log_perm = p001.stdout.read().strip()

    logging.info("step2:查看uos用户组信息是否不包含adm")
    cmd2 = r"groups uos | awk -F: '{print $2}'"
    p002 = subprocess.Popen(cmd2,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    groups_lst = p002.stdout.read().strip().split(" ")

    logging.info("step3:检查uos管理员是否对auth.log没有读权限")
    cmd3 = r"cat /var/log/auth.log"
    p003 = subprocess.run(cmd3,
                          shell=True,
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          encoding='utf-8')
    uos_cat_code = p003.returncode

    logging.info("step4:检查sudo提权后是否对auth.log有读权限")
    cmd4 = r"echo 1 | sudo -S cat /var/log/auth.log"
    p004 = subprocess.run(cmd4,
                          shell=True,
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          encoding='utf-8')
    root_cat_code = p004.returncode

    if auth_log_perm == "-rw-r----- root adm" and "adm" not in groups_lst and uos_cat_code == 1 and root_cat_code == 0:
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        logging.error("检查auth.log权限异常，请检查：")
        logging.debug(auth_log_perm)
        logging.debug(groups_lst)
        logging.debug(uos_cat_code)
        logging.debug(root_cat_code)
        assert False
