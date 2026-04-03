#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          601047
# @Test Description:      用户登陆模块采用SHA-512加密算法
# @Test Condition:
# @Test Step:            1.查看用户登录模块采用的加密算法
# @Test expect Result:   1.用户登录模块采用SHA-512加密算法
'''
保存方式为username:$id$salt$encrypted,例如：
uos:$6$yTo44Yaopea2eKTQ$QkRcnetJxr3kExfpb5okD5qXHLjaC1N3rVsVu7ZZxbBeE2HCvaWc51MBgzceV8uNA/fV8fe/fhk58QjJD1vYw/:18932:0:99999:7:::
其中id=6代表采用的密码算法为SHA-512。1对应MD5,2a对应BlowFish,5对应SHA-256,6对应SHA-512。SHA-512在密码算法推荐清单'优先推荐'列表中
'''
# @Test Remark:
# @Author:  杨浪_ut001228
# @Date: 2022/4/14
# *****************************************************
import sys
import pytest
import logging
import subprocess

from frame.common import system_kernel_log_cap, execute_command


def get_current_username():
    username = execute_command("whoami").strip("\n").replace("请输入密码",
                                                             "").replace(
                                                                 "验证成功", "")
    return username


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_usr_login_encrypt_601047():
    logging.info("step1:查看用户登录模块采用的加密算法")
    encryption_algo_lst = {
        "6": "SHA-512",
        "1": "MD5",
        "2a": "BlowFish",
        "5": "SHA-256"
    }

    cmd1 = "echo 1|sudo -S cat /etc/shadow | grep " + get_current_username(
    ) + "|awk -F '$' '{print $2}'"

    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    res1 = p001.stdout.read().strip("\n").replace("请输入密码",
                                                  "").replace("验证成功", "")

    logging.info("用户登录模块采用的加密算法为" + encryption_algo_lst[res1])

    if res1 == "6":
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        logging.error("step1:用户登录模块采用的加密算法不为SHA-512,请检查！")
        assert False
