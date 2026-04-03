#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:      598603
# @Test Description:  禁止除列表之外目录被不同本地账户共同读写
# @Test Condition:
# @Test Step:
# 使用root用户，检查不同本地账户共用的读写目录
# find / -type d \( -perm -006 -a -perm -060 \) -ls 2>/dev/null|awk '{print $11}'
# @Test expect Result:
# 不同本地账户共用的读写目录只有如下：
'''
/run/lock
/dev/mqueue
/dev/shm
/tmp
1040添加例外的目录:
/var/spool/samba  drwxrwxrwx
'''
# @Test Remark:
# @Author: ut002037
# *****************************************************
import sys
import pytest
import logging
import subprocess
import re

from frame.common import open_excel_file
from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_rw_dir_for_all_user_598603():
    expect_dir_lst = []
    expect_dir_random_str_pattern_lst = []
    bug_dir_lst = []
    # 打开待操作的sheet表单
    sheet_op = open_excel_file("./configs/系统基线规范.xlsx", "dir.white")
    max_row = sheet_op.max_row
    for row in range(2, max_row + 1):
        dir_name = sheet_op.cell(row=row, column=1).value
        random_str = sheet_op.cell(row=row, column=2).value
        if dir_name is None:
            break
        if int(random_str) == 1:
            expect_dir_random_str_pattern_lst.append(
                re.compile(dir_name.strip(" \n")))
        elif int(random_str) == 2:
            bug_dir_lst.append(dir_name.strip(" \n"))
        else:
            expect_dir_lst.append(dir_name.strip(" \n"))

    cmd1 = r"echo 1|sudo -S find / -type d \( -perm -006 -a -perm -060 \) -ls 2>/dev/null|awk '{print $11}'"

    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    tmp = p001.stdout.read().replace("请输入密码", "").replace("验证成功", "")
    acture_dir_lst = tmp.strip().split("\n")

    dir_tmp = list(set(acture_dir_lst) - set(expect_dir_lst))
    logging.debug(dir_tmp)

    for i in dir_tmp:
        for pattern in expect_dir_random_str_pattern_lst:
            str1 = re.match(pattern, i)
            if str1 is None:
                continue
            else:
                expect_dir_lst.append(str1.group())
    logging.debug(expect_dir_lst)

    # 由于home lost+found opt root var目录都是挂载到/data上的，实际是一份，所以这里做下特殊处理
    for i in expect_dir_lst:
        if i[0:4] == "/var":
            dir = "/data" + i
            expect_dir_lst.append(dir)

    perror_info = list(set(acture_dir_lst) - set(expect_dir_lst) - set(bug_dir_lst))
    if len(perror_info) != 0:
        logging.error(perror_info)
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
    else:
        assert True
