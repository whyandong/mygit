#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:     846121
# @Test Description: 检查被赋予特权的系统服务
# @Test Condition:
# @Test Step:       sudo grep =CAP /usr/lib/systemd/system/* /usr/lib/systemd/user/* 2>/dev/null | grep -v "#"
# @Test expect Result: 与系统基线数据进行对比,无新增也无减少
# @Test Remark:
# @Author: ut002037
# *****************************************************
import sys
import pytest
import logging
import subprocess

from frame.common import open_excel_file
from frame.common import get_platform_arch
from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_service_check_cap_846121():
    expect_service_cap_lst = []
    # 获取系统架构
    sys_arch = get_platform_arch()
    # 打开待操作的sheet表单
    sheet_op = open_excel_file("./configs/系统基线规范.xlsx", "sys_cap")
    max_row = sheet_op.max_row
    for row in range(2, max_row + 1):
        arch = sheet_op.cell(row=row, column=2).value
        # print(arch)
        if arch is None:
            break
        elif arch.strip("\n") == "all" or arch.strip("\n") in sys_arch:
            file_type = sheet_op.cell(row=row, column=3).value.strip("\n")
            if "service" in file_type.lower():
                bin_cap = sheet_op.cell(row=row, column=1).value.strip("\n")
                expect_service_cap_lst.append(bin_cap)
        else:
            continue
    logging.info(f"当前获取的基线能力数据是{expect_service_cap_lst}")

    cmd1 = r'echo 1|sudo -S grep =CAP /usr/lib/systemd/system/* /usr/lib/systemd/user/* 2>/dev/null | grep -v "#"'
    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    tmp = p001.stdout.read().replace("请输入密码", "").replace("验证成功", "")
    acture_service_cap_lst = tmp.strip().split("\n")

    tmp1 = list(set(acture_service_cap_lst) - set(expect_service_cap_lst))
    tmp2 = list(set(expect_service_cap_lst) - set(acture_service_cap_lst))
    if len(tmp1) == 0 and len(tmp2) == 0:
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        logging.error(f"实际多了{tmp1}")
        logging.error(f"实际少了{tmp2}")
        assert False
