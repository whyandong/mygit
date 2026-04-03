#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:      598649
# @Test Description:  deb软件包仓库源-写保护
# @Test Condition:
# @Test Step:         ls -al /etc/apt/sources.list | awk '{print $1}'
# @Test expect Result:-rw-r--r--
# @Test Remark:
# @Author:  汪晓刚_ut002037
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


def test_src_file_write_protect_598649():
    file_lst = []
    expect_perm_lst = []
    acture_perm_lst = []
    # 获取系统架构
    sys_arch = get_platform_arch()
    # 打开待操作的sheet表单
    sheet_op = open_excel_file("./configs/系统基线规范.xlsx",
                               "src_lst_file_write_protect")
    max_row = sheet_op.max_row
    for row in range(2, max_row):
        arch = sheet_op.cell(row=row, column=3).value
        # print(arch)
        if arch is None:
            break
        elif arch.strip("\n") == "all" or arch.strip("\n") in sys_arch:
            file = sheet_op.cell(row=row, column=1).value.strip("\n")
            file_lst.append(file)
            perm = sheet_op.cell(row=row,
                                 column=2).value.strip("\n").strip("'")
            expect_perm_lst.append(perm)
            # print(expect_user_lst)
        else:
            continue

    for file in file_lst:
        cmd1 = "ls -al " + file + "| awk '{print $1}'"
        p001 = subprocess.Popen(cmd1,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding='utf-8')
        tmp = p001.stdout.read().replace("请输入密码", "").replace("验证成功", "")
        acture_perm_lst.append(tmp.strip().strip("\n"))

    # if len(acture_user_lst) == len(expect_user_lst):
    if len(list(set(acture_perm_lst) - set(expect_perm_lst))) == 0:
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        logging.error((set(acture_perm_lst) - set(expect_perm_lst)))
        assert False
