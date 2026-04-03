#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:      598673
# @Test Description:    检查系统中的服务配置文件是否被异常修改
# @Test Condition:    all
# @Test Step:       1.获取服务配置文件md5基线数据 2.获取本机系统服务的md5信息
# @Test expect： 参考uniontest/configs/系统基线规范.xlsx
# @Test Remark:
# @Author:  ut000220
# @Date:    2022/5/20
# *****************************************************

import logging
from struct import pack_into
import sys
import pytest
import subprocess

from frame.common import open_excel_file
from frame.common import system_kernel_log_cap
from frame.common import get_platform_arch
from frame.common import get_packet_name_from_path
from frame.common import get_packet_version


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_check_service_conf_598673():
    # 打开待操作的sheet表单
    expect_service_conf_lst = []
    service_conf_lst = []
    sys_arch = get_platform_arch()
    bug_conf_lst = []

    sheet_op = open_excel_file("./configs/系统基线规范.xlsx", "service_conf")
    max_row = sheet_op.max_row
    for row in range(2, max_row + 1):
        arch = sheet_op.cell(row=row, column=3).value
        # logging.debug(arch)
        if arch is None:
            break
        elif "all" in arch.strip(" \n") or sys_arch in arch.strip(" \n"):
            md5 = sheet_op.cell(row=row, column=1).value.strip()
            service_name = sheet_op.cell(row=row, column=2).value.strip()
            expect_service_conf_lst.append(md5 + '  ' + service_name)
        elif "bug" in arch.strip(" \n"):
            md5 = sheet_op.cell(row=row, column=1).value.strip()
            service_name = sheet_op.cell(row=row, column=2).value.strip()
            bug_conf_lst.append(md5 + '  ' + service_name)

    logging.debug(f"step1: 获取服务配置文件md5基线数据如下:\n{expect_service_conf_lst}")

    cmd1 = r"md5sum /lib/systemd/system/*.service /lib/systemd/user/*.service | sort -k2"
    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    service_conf_lst = p001.stdout.read().strip().split("\n")
    logging.debug(f"step2:获取本机服务配置md5信息:\n{service_conf_lst}")

    service_conf_err = list(
        set(service_conf_lst) - set(expect_service_conf_lst) - set(bug_conf_lst))
    service_conf_err_num = len(service_conf_err)

    service_lost_check = list(
        set(expect_service_conf_lst) - set(service_conf_lst))
    logging.error(f"系统减少了如下几个服务配置:{service_lost_check}")

    if service_conf_err_num == 0:
        assert True
    else:
        logging.error("存在" + str(service_conf_err_num) + "个异常配置的服务:")
        logging.error(f"系统修改或新增了如下几个服务配置:{service_conf_err}")
        for i in service_conf_err:
            path = i.split("  ")[-1]
            pack_name = get_packet_name_from_path(path)
            logging.error(get_packet_version(pack_name))
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
