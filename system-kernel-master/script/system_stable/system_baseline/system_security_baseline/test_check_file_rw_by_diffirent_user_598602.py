#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:     598602
# @Test Description:禁止除/sys、/proc、/dev目录之外被不同本地账号共同读写的文件
# @Test Condition: 默认新装系统
# @Test Step: sudo find / \( -path /sys -o -path /dev -o -path /proc \) -prune -o -type f \( -perm -006 -a -perm -060 \) -ls 2>/dev/null
# @Test expect Result: 查询为空，没有被不同本地账号读写的文件
# @Test Remark:
# @Author: ut002037
# @Date: 2022/5/23
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


def test_check_file_rw_by_diffirent_user_598602():
    cmd1 = r"echo 1|sudo -S find / \( -path /sys -o -path /dev -o -path /proc \) -prune -o -type f \( -perm -006 -a -perm -060 \) -ls 2>/dev/null"
    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    res1 = p001.stdout.read().replace("请输入密码", "").replace("验证成功", "")
    if not res1:
        logging.info(res1)
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        logging.error("存在/sys、/proc、/dev目录之外被不同本地账号共同读写的文件" + str(res1))
        assert False
