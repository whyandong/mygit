#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          601085
# @Test Description:      dev-hugepages.mount 系统挂载大页服务测试
# @Test Condition:
# @Test Step:           1.检查dev-hugepages.mount服务默认状态 2.关闭dev-hugepages.mount服务检查状态 3.开启dev-hugepages.mount服务检查状态 4.检查hugetlbfs模块是否正常挂载
# @Test expect Result:  1.服务默认状态为active 2.关闭后服务状态为inactive 3.开启后服务状态为active 4.hugetlbfs模块正常挂载
# @Test Remark:
# @Author:  夏曙_ut000220
# @Date:    2021/12/20
# *****************************************************
import sys
import os
import pytest
import logging

from frame.common import execute_command
from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enable stage !")
    yield
    logging.info("this is env disable stage !")


def test_hugepages_service_601085():
    cmd1 = "systemctl status dev-hugepages.mount | grep Active | awk -F ':' '{print$2}' | awk -F ' ' '{print$1}'"

    hugepages_status = execute_command(cmd1)

    logging.info("step1:检查服务默认状态是否为active")

    if "active" in hugepages_status:
        assert True
    else:
        logging.error("服务默认状态不是active,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False

    os.system("echo 1 | sudo -S systemctl stop dev-hugepages.mount")

    hugepages_status = (execute_command(cmd1)).split()

    logging.info("step2:检查执行关闭服务操作后, 服务状态是否为inactive")

    if "inactive" in hugepages_status:
        assert True
    else:
        logging.error("执行关闭服务操作后, 服务状态不是inactive,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False

    os.system("echo 1 | sudo -S systemctl start dev-hugepages.mount")

    hugepages_status = (execute_command(cmd1)).split()

    logging.info("step3:检查执行开启服务操作后, 服务状态是否为active")

    if "active" in hugepages_status:
        assert True
    else:
        logging.error("执行开启服务操作后, 服务状态不是active,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False

    hugetlbfs_mount = (execute_command("mount | grep hugetlbfs")).split()

    logging.info("step4:检查hugetlbfs模块是否正常挂载")

    if "hugetlbfs" in hugetlbfs_mount:
        assert True
    else:
        logging.error("检查hugetlbfs模块挂载状态失败, hugetlbfs模块没有挂载")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
