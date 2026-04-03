#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:     844023
# @Test Description: getcap检查系统被赋予特权的文件
# @Test Condition:
# @Test Step:        echo 1|sudo -S getcap -r / 检查系统被赋予特权的文件
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


def test_bin_check_cap_844023():
    expect_bin_cap_lst = []
    bug_bin_cap_lst = []
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
            if "bin" in file_type.lower():
                bin_cap = sheet_op.cell(row=row, column=1).value.strip("\n")
                expect_bin_cap_lst.append(bin_cap)
            elif "bug" in file_type.lower():
                bug_cap = sheet_op.cell(row=row, column=1).value.strip("\n")
                bug_bin_cap_lst.append(bug_cap)
        else:
            continue
    logging.info(f"当前获取的基线能力数据是{expect_bin_cap_lst}")

    cmd1 = "echo 1|sudo -S getcap -r / 2>/dev/null"
    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    tmp = p001.stdout.read().replace("请输入密码", "").replace("验证成功", "")
    # 过滤掉cap能力为空的元素
    acture_bin_cap_lst = [x for x in tmp.strip().split("\n") if x.split("=")[1] != ""]

    tmp1 = list(set(acture_bin_cap_lst) - set(expect_bin_cap_lst)- set(bug_bin_cap_lst))
    tmp2 = list(set(expect_bin_cap_lst) - set(acture_bin_cap_lst))
    if len(tmp1) == 0 and len(tmp2) == 0:
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        logging.error(f"实际多了{tmp1}")
        logging.error(f"实际少了{tmp2}")
        assert False
