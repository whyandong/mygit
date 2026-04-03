#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          602957
# @Test Description:      iptables保存规则测试
# @Test Condition:        安装iptables-persistent
# @Test Step:
# 1.任意添加一条规则：如echo  1 | sudo -S  iptables -A INPUT -s 1.1.1.1/24 -j ACCEPT
# 2.执行sudo netfilter-persistent save，执行echo  1 | sudo -S  cat /etc/iptables/rules.v4
# 3.echo 1 | sudo -S iptables -nvL | grep '1.1.1.0/24' | awk '{print $8}'
# 4.清除规则：echo 1 | sudo -S  iptables -F，再查看规则：echo 1 | sudo -S iptables -nvL | grep '1.1.1.0/24' | awk '{print $8}'
# 5.载入规则sudo netfilter-persistent reload
# 6.再查看规则：echo 1 | sudo - S iptables - nvL | grep '1.1.1.0/24' | awk '{print $8}'
# @Test expect Result:
# 6.正常载入规则，打印：1.1.1.0/24
# @Test Remark:
# @Author: 杨浪_ut001228
# Date: 2022/5/26
# *****************************************************
import os
import sys
import pytest
import logging

from frame.common import execute_command
from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    os.system("echo 1|sudo -S apt-get install -y iptables-persistent")
    yield
    os.system("echo 1|sudo - S iptables - F")
    os.system("echo 1|sudo -S systemctl stop netfilter-persistent.service")
    os.system("echo 1|sudo -S systemctl disable netfilter-persistent.service")
    os.system("echo 1|sudo -S dpkg -P iptables-persistent")
    os.system("echo 1|sudo -S apt remove --purge iptables-persistent")


def test_iptables_save_602957():
    logging.info("step1:添加一条规则")
    os.system("echo  1 | sudo -S  iptables -A INPUT -s 1.1.1.1/24 -j ACCEPT")

    logging.info("step2:保存规则并检查是否保存成功")
    os.system("echo 1|sudo -S netfilter-persistent save")

    logging.info("确认规则文件保存到了/etc/iptables/rules.v4文件里!")
    if os.system("echo 1|sudo -S cat /etc/iptables/rules.v4|grep '1.1.1.0/24'"
                 ) != 0:
        logging.error("保存规则文件到/etc/iptables/rules.v4失败!")
        assert False
    else:
        assert True

    check1 = execute_command(
        "echo 1 | sudo -S iptables -nvL | grep '1.1.1.0/24' | awk '{print $8}'"
    )
    logging.info("保存规则为:" + check1)
    if "1.1.1.0/24" in check1:
        assert True
    else:
        logging.error("保存规则错误:" + check1)
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False

    logging.info("step3:清除规则并检查")
    os.system("echo 1 | sudo -S iptables -F")
    check2 = execute_command(
        "echo 1 | sudo -S iptables -nvL | grep '1.1.1.0/24' | awk '{print $8}'"
    )

    logging.info("清除规则为:" + check2)
    if "" in check2:
        assert True
    else:
        logging.error("清除规则错误:\n" + check1)
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False

    os.system("echo 1|sudo -S netfilter-persistent reload")

    check3 = execute_command(
        "echo 1 | sudo -S iptables -nvL | grep '1.1.1.0/24' | awk '{print $8}'"
    )

    logging.info("重新加载规则为:\n" + check3)
    if "1.1.1.0/24" in check3:
        assert True
    else:
        logging.error("重新加载规则错误:\n" + check1)
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
