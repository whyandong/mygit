#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:  601060
# @Test Description:
# @Test Condition:
# @Test Step: 查看开机自启动服务，执行sudo systemctl list-unit-files | grep service | grep enabled与系统服务申请入口中已申请的服务列表进行对比（或与系统基线数据对比
# @Test expect Result: 没有未经评审的自启动服务
# @Test Remark:
# @Author: ut002037
# *****************************************************
import sys
import pytest
import logging
import subprocess

from frame.common import open_excel_file
from frame.common import system_kernel_log_cap, get_platform_arch


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_check_sys_startup_service_601060():
    expect_startup_service_lst = []
    cd_service = []
    bug_service = []
    # 获取系统架构
    sys_arch = get_platform_arch()
    # 打开待操作的sheet表单
    sheet_op = open_excel_file("./configs/系统基线规范.xlsx", "系统服务")
    max_row = sheet_op.max_row
    for row in range(2, max_row + 1):
        arch = sheet_op.cell(row=row, column=2).value
        # print(arch)
        if arch is None:
            break
        elif arch.strip("\n").lower() == "all" or sys_arch in arch.strip("\n"):
            service = sheet_op.cell(row=row, column=1).value.strip("\n")
            expect_startup_service_lst.append(service)
        elif arch.strip("\n").lower() == 'cd':
            logging.debug(arch.strip("\n").lower())
            service = sheet_op.cell(row=row, column=1).value.strip("\n")
            cd_service.append(service)
        elif arch.strip("\n").lower() == 'bug':
            logging.debug(arch.strip("\n").lower())
            service = sheet_op.cell(row=row, column=1).value.strip("\n")
            bug_service.append(service)
        else:
            continue

    logging.info("step2:获取系统自启动服务列表")
    cmd1 = "systemctl list-unit-files | grep enabled | grep service | awk '{print $1}'"
    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    acture_startup_service_lst = [
        x for x in p001.stdout.read().replace("请输入密码", "").replace(
            "验证成功", "").split("\n") if x != ''
    ]

    logging.debug(acture_startup_service_lst)
    logging.debug(expect_startup_service_lst)
    tmp = list(
        set(acture_startup_service_lst) - set(expect_startup_service_lst) - set(cd_service) - set(bug_service))
    tmp1 = list(
        set(expect_startup_service_lst) - set(acture_startup_service_lst))

    if len(tmp) == 0 and len(tmp1) == 0:
        assert True
    else:
        logging.error(f"多了自启服务:{tmp}")
        logging.error(f"少了自启服务:{tmp1}")
        logging.error(f"bug引入服务:{bug_service}")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
