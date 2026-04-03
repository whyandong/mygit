#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          302386
# @Test Description:       rsyslog的年份检查
# @Test Condition:
# @Test Step:          /etc/rsyslog.cfg md5对比检查，与历史基线版本
# @Test expect Result: 与历史基线对比无变化，有变化的需要与开发确认，变化内容并更新基线数据
# @Test Remark:
# @Author:ut002037
# *****************************************************
import sys
import pytest
import logging
import subprocess

from frame.common import get_platform_arch
from frame.common import system_kernel_log_cap, open_excel_file


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_rsyslog_cfg_check_302386():
    # 获取系统架构,针对龙芯机器做处理，架构统一为mips
    sys_arch = get_platform_arch()
    cfg_file = "/etc/rsyslog.conf"
    if "mips" in sys_arch or "loongarch" in sys_arch:
        sys_arch = "mips"
    # 打开待操作的sheet表单
    sheet_op = open_excel_file("./configs/系统基线规范.xlsx", "cfg_file_md5_sum")
    max_row = sheet_op.max_row
    for row in range(2, max_row + 1):
        cfg_file_path = sheet_op.cell(row=row, column=1).value
        logging.debug(cfg_file_path)
        if cfg_file_path is None:
            break
        elif cfg_file in cfg_file_path:
            arch = sheet_op.cell(row=row, column=3).value
            if "all" in arch or sys_arch in arch.strip(" \n"):
                expect_md5 = sheet_op.cell(row=row,
                                           column=2).value.strip(" \n")
                break
        else:
            continue

    get_current_md5 = r"echo 1|sudo -S md5sum " + cfg_file + "|awk '{print $1}'"
    p001 = subprocess.Popen(get_current_md5,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    current_md5 = p001.stdout.read().replace("请输入密码", "").replace("验证成功",
                                                                  "").strip()

    logging.debug("current_md5:" + current_md5)
    logging.debug("expect_md5:" + expect_md5)
    if current_md5 == expect_md5:
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
