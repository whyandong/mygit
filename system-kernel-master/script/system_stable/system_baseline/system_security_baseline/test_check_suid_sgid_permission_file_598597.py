#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          598597
# @Test Description:      检查拥有suid/sgid权限的文件
# @Test Condition:
# @Test Step:           echo 1|sudo -S find / -perm /6000 -ls -xdev 2>/dev/null
# @Test expect Result: 与系统基线数据进行对比,无新增sgid，suid的文件，新增文件都经过评审备案
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


def test_check_suid_sgid_permission_file_598597():
    expect_suid_sgid_lst = []
    bug_suid_sgid_lst = []
    # 获取系统架构
    sys_arch = get_platform_arch()
    # 打开待操作的sheet表单
    sheet_op = open_excel_file("./configs/系统基线规范.xlsx", "suid_sgid")
    max_row = sheet_op.max_row
    for row in range(2, max_row + 1):
        arch = sheet_op.cell(row=row, column=3).value
        # print(arch)
        if arch is None:
            break
        elif arch.strip("\n") == "all" or arch.strip("\n") in sys_arch:
            user = sheet_op.cell(row=row, column=1).value.strip("\n")
            expect_suid_sgid_lst.append(user)
            # print(expect_user_lst)
        elif "bug" in arch.strip("\n"):
            user = sheet_op.cell(row=row, column=1).value.strip("\n")
            bug_suid_sgid_lst.append(user)
        else:
            continue

    cmd1 = "echo 1|sudo -S find / -perm /6000 -ls -xdev 2>/dev/null|awk '{print $NF}'"

    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    tmp = p001.stdout.read().replace("请输入密码", "").replace("验证成功", "")
    acture_suid_sgid_lst = tmp.strip().split("\n")

    test = []
    temp = list(set(acture_suid_sgid_lst) - set(expect_suid_sgid_lst) - set(bug_suid_sgid_lst))
    for i in temp:
        if "/usr/local/lib/python3" not in i:
            test.append(i)
    if len(test) == 0:
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        logging.error("实际多了" + str(test))
        assert False
