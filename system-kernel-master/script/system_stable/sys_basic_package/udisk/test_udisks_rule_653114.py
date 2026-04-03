#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          653114
# @Test Description:
# @Test Condition:        版本>=1050
# @Test Step:            1.获取udisks规则基线数据 2.获取系统udisks规则数据,与步骤1的结果对比
# @Test expect Result:   1.正常获取 2.对比无差异
# @Test Remark:
# @Author:  夏曙_ut000220
# @Date: 2022/5/18
# *****************************************************
import sys
import os
import pytest
import logging
import subprocess
from frame.common import open_excel_file, get_platform_arch
from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    os.system("apt policy pulseaudio")
    yield
    logging.info("this is env disable stage !")


def test_udisks_rule_653114():
    # 获取系统架构,针对龙芯机器做处理，架构统一为mips
    sys_arch = get_platform_arch()
    # 打开待操作的sheet表单
    expect_lst = []
    random_lst = []
    udisks_rule_lst = []
    sheet_op = open_excel_file("./configs/系统基线规范.xlsx", "udisks.rule")
    logging.info("step1: 获取udisks规则基线数据:")
    max_row = sheet_op.max_row
    # logging.debug(sys_arch)
    for row in range(2, max_row + 1):
        arch = sheet_op.cell(row=row, column=3).value
        if arch is None:
            break
        elif "all" in arch.strip() or sys_arch in arch.strip():
            md5 = sheet_op.cell(row=row, column=1).value.strip("\n")
            file = sheet_op.cell(row=row, column=2).value.strip("\n")
            random = sheet_op.cell(row=row, column=4).value
            if int(random):
                random_lst.append(file)
            else:
                expect_lst.append(md5 + '  ' + file)
        else:
            continue
    logging.debug(f"系统基线数据:{expect_lst}")

    logging.info("step2: 获取系统udisks规则数据:")
    cmd = r"md5sum /etc/udev/rules.d/* /usr/lib/udev/rules.d/* | sort -k2"
    p001 = subprocess.Popen(cmd,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    udisks_rule_lst = p001.stdout.read().strip().split("\n")
    # 去掉跟硬件相关（md5值不固定）的元素的md5值，只比较文件名，检查该文件是否存在即可
    for j in random_lst:
        for k in udisks_rule_lst:
            if j in k:
                udisks_rule_lst.remove(k)
                continue

    logging.debug(f"系统当前数据:{udisks_rule_lst}")

    udisks_rule_err = list(set(expect_lst) - set(udisks_rule_lst))
    udisks_rule_add = list(set(udisks_rule_lst) - set(expect_lst))

    logging.info("系统存在udisks规则新增:")
    logging.info(udisks_rule_add)

    if len(udisks_rule_err) == 0:
        assert True
    else:
        logging.error("系统存在udisks规则文件缺失:")
        logging.error(udisks_rule_err)
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
