#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
# ****************************************************
# @Test Case ID:         247711
# @Test Description:     /根目录结构规范性检查
# @Test Condition:  root_lists=("." ".." "bin" "boot" "dev" "etc" "home" "lib" "lib32" "lib64" "libx32" "media" "mnt" "opt"
# "proc" "recovery" "root" "run" "sbin" "srv" "sys" "tmp" "usr" "var" "data" "lost+found")
# @Test Step:           1.sudo cd /;ls -a   2比较第一步返回的结果是否与预置条件里的结果
# @Test expect Result:          第一步返回的结果与根目录规范定义的目录结构一致，没有多的也没少的
# @Test Remark:
# @Author:  汪晓刚_ut002037
# *****************************************************
import sys
import pytest
from frame.common import open_excel_file, get_platform_arch
from frame.common import execute_command, system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_check_dir_struct_247711():
    expect_root_dir_needed_lst = []
    expect_root_dir_unneeded_lst = []
    cd_dir_lst = []

    # 获取系统架构,针对龙芯机器做处理，架构统一为mips
    sys_arch = get_platform_arch()

    # 打开待操作的sheet表单
    sheet_op = open_excel_file("./configs/系统基线规范.xlsx", "目录规范")
    max_row = sheet_op.max_row
    for row in range(2, max_row + 1):
        arch = sheet_op.cell(row=row, column=2).value
        logging.debug(arch)
        if arch is None:
            break
        elif "all" in arch.strip(" \n") or sys_arch in arch.strip(" \n"):
            dir_name = sheet_op.cell(row=row, column=1).value.strip(" \n")
            if int(sheet_op.cell(row=row, column=3).value):
                expect_root_dir_needed_lst.append(dir_name)
            else:
                expect_root_dir_unneeded_lst.append(dir_name)
        elif "cd" in arch.lower().strip(" \n"):
            dir_name = sheet_op.cell(row=row, column=1).value.strip(" \n")
            cd_dir_lst.append(dir_name)
        else:
            continue

    cmd1 = 'cd /;ls -a'
    home_dir = (execute_command(cmd1)).split()
    step1 = "step1 exec " + cmd1 + " return home_dir list:"
    logging.debug(str(step1))
    logging.debug(home_dir)

    acture_dir_lst = list(set(home_dir) - set(expect_root_dir_unneeded_lst) - set(cd_dir_lst))
    logging.debug(acture_dir_lst)
    logging.debug(expect_root_dir_needed_lst)
    tmp1 = list(set(acture_dir_lst) - set(expect_root_dir_needed_lst))
    tmp2 = list(set(expect_root_dir_needed_lst) - set(acture_dir_lst))
    if len(tmp1) == 0 and len(tmp2) == 0:
        assert True
    elif len(tmp1) or len(tmp2) != 0:
        logging.error("根目录结构与预期大小不一致:")
        logging.error("多出目录:" + str(tmp1))
        logging.error("少了目录:" + str(tmp2))
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
