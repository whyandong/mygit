#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:      476640
# @Test Description:  检查系统中所属组为shadow的文件
# @Test Condition:
# @Test Step:
# 使用root用户，查找系统中所属组为shadow的文件
# echo 1|sudo -S find / -group shadow -xdev 2>/dev/null
# @Test expect Result:
'''
以1030的结果为参考:
/usr/bin/chage
/usr/bin/expiry
/usr/sbin/unix_chkpwd
/etc/shadow-
/etc/gshadow
/etc/gshadow-
/etc/shadow

与1030版本对比,查找出所属组为shadow的文件没有增多
'''
# @Test Remark:
# @Author: ut002037
# *****************************************************

import sys
import pytest
import logging
import subprocess

from frame.common import open_excel_file
from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_check_the_files_in_the_system_whose_group_is_shadow_476640():
    expect_file_lst = []
    # 打开待操作的sheet表单
    sheet_op = open_excel_file("./configs/系统基线规范.xlsx", "file_group_shadow")
    max_row = sheet_op.max_row
    for row in range(2, max_row + 1):
        file = sheet_op.cell(row=row, column=1).value
        if file is None:
            break
        else:
            expect_file_lst.append(file.strip(' \n'))

    cmd1 = r"echo 1|sudo  -S  find / -group shadow -xdev 2>/dev/null"
    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    acture_file_lst = p001.stdout.read().replace("验证成功", "").replace(
        "请输入密码", "").strip().split("\n")

    logging.debug(acture_file_lst)
    logging.debug(expect_file_lst)
    result = list(set(acture_file_lst) - set(expect_file_lst))
    logging.debug(result)
    if len(result) != 0:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
    else:
        assert True
