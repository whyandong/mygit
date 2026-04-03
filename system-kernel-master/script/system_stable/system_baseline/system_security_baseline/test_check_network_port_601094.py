#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:      601094
# @Test Description:
# @Test Condition:    all
# @Test Step:       netstat -lntup
# @Test expect： 参考uniontest/configs/系统基线规范.xlsx
# @Test Remark:
# @Author:  ut000220
# @Date:    2022/5/7
# *****************************************************

import logging
import sys
import pytest
import subprocess

from frame.common import open_excel_file, get_platform_arch
from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_check_network_port_601094():
    sys_arch = get_platform_arch()
    # 打开待操作的sheet表单
    expect_port_lst = []
    cd_port_lst = []
    expect_random_port = {}
    sheet_op = open_excel_file("./configs/系统基线规范.xlsx", "端口监听")
    max_row = sheet_op.max_row
    for row in range(2, max_row + 1):
        arch = sheet_op.cell(row=row, column=1).value
        # print(arch)
        if arch is None:
            break
        elif "all" in arch.strip(" \n") or sys_arch in arch.strip(" \n"):
            proto = sheet_op.cell(row=row, column=2).value.strip(" \n")
            local_addr = sheet_op.cell(row=row, column=3).value.strip(" \n")
            pname = sheet_op.cell(row=row, column=4).value.strip(" \n")
            random = sheet_op.cell(row=row, column=5).value
            if int(random):
                expect_random_port.update({proto: pname})
            else:
                expect_port = proto + ' ' + local_addr + ' ' + pname
                expect_port_lst.append(expect_port)
        elif "cd" in arch.strip(" \n").lower():
            proto = sheet_op.cell(row=row, column=2).value.strip(" \n")
            local_addr = sheet_op.cell(row=row, column=3).value.strip(" \n")
            pname = sheet_op.cell(row=row, column=4).value.strip(" \n")
            expect_port = proto + ' ' + local_addr + ' ' + pname
            cd_port_lst.append(expect_port)
        else:
            continue

    logging.info(f"step1: 获取监听端口基线数据：{expect_port_lst}")
    logging.info(f"获取CD打开的监听端口基线数据：{cd_port_lst}")

    logging.info("step2:获取本机协议与端口号：")
    cmd1 = r"echo 1 | sudo -S netstat -lntup | sed -n '3,$p' | awk '{print $1,$4}'"
    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    res1 = p001.stdout.read().replace("验证成功",
                                      "").replace("请输入密码",
                                                  "").strip().split("\n")
    print(res1)

    logging.info("step3:获取本机占用端口的进程名:")
    cmd2 = r"echo 1 | sudo -S netstat -lntup | sed -n '3,$p' | cut -d '/' -f2-"
    p002 = subprocess.Popen(cmd2,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    res2 = p002.stdout.read().replace("验证成功",
                                      "").replace("请输入密码",
                                                  "").strip().split("\n")

    sys_port_list = [
        i.strip() + ' ' + j.strip() for i, j in list(zip(res1, res2))
    ]
    logging.info(f"step4: 当前系统监听端口:{sys_port_list}")

    port_err = list(
        set(sys_port_list) - set(expect_port_lst) - set(cd_port_lst))
    for key, value in expect_random_port.items():
        for i in port_err:
            if key in i and value in i:
                port_err.remove(i)

    if len(port_err) == 0:
        assert True
    else:
        logging.error(f"系统存在未经评审的默认监听端口:{port_err}")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
