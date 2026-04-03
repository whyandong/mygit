#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          602937
# @Test Description:      系统预置帐号检查
# @Test Condition:
# @Test Step:            1.检查系统预置账号
# @Test expect Result:   1.预置账号中
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


def test_pre_user_check_602937():
    expect_user_lst = []
    cd_user = []
    # 获取系统架构
    sys_arch = get_platform_arch()
    # 打开待操作的sheet表单
    sheet_op = open_excel_file("./configs/系统基线规范.xlsx", "系统预置账号")
    max_row = sheet_op.max_row
    for row in range(2, max_row + 1):
        arch = sheet_op.cell(row=row, column=2).value
        # print(arch)
        if arch is None:
            break
        elif arch.strip("\n") == "all" or sys_arch in arch.strip("\n"):
            user = sheet_op.cell(row=row, column=1).value.strip("\n")
            expect_user_lst.append(user)
            # print(expect_user_lst)
        elif arch.strip("\n").lower() == 'cd':
            logging.debug(arch.strip("\n").lower())
            user = sheet_op.cell(row=row, column=1).value.strip("\n")
            cd_user.append(user)
        else:
            continue

    cmd1 = "echo 1|sudo -S cat /etc/group | awk -F ':' '{print $1}'"

    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    tmp = p001.stdout.read().replace("请输入密码", "").replace("验证成功", "")
    acture_user_lst = [x for x in tmp.strip().split("\n") if x != '']
    logging.debug(acture_user_lst)
    logging.debug(expect_user_lst)

    # if len(acture_user_lst) == len(expect_user_lst):
    if len(list(set(acture_user_lst) - set(expect_user_lst) -
                set(cd_user))) == 0 and len(
                    list(
                        set(expect_user_lst) - set(acture_user_lst) -
                        set(cd_user))) == 0:
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        logging.error(
            "实际多了" +
            str(set(acture_user_lst) - set(expect_user_lst) - set(cd_user)))
        logging.error(
            "预期少了" +
            str(set(expect_user_lst) - set(acture_user_lst) - set(cd_user)))
        assert False
