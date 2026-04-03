#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:     631311
# @Test Description:【all】【兼容性测试】【升级专项测试】【pulseaudio】配置文件检查（与基线对比）
# @Test Condition:
# @Test Step:
'''获取pulseaudio配置文件列表:
find /usr/share/pulseaudio/alsa-mixer/profile-sets > pulseaudio_profile-sets.conf
find /usr/share/pulseaudio/alsa-mixer/paths > pulseaudio_paths.conf'''
# @Test expect Result: 与基线对比没有更改
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


def test_pulseaudio_cfg_check_631311():
    expect_profile_lst = []
    expect_path_lst = []
    # 获取系统架构
    sys_arch = get_platform_arch()
    # 打开待操作的sheet表单
    sheet_op = open_excel_file("./configs/系统基线规范.xlsx", "audio_config")
    max_row = sheet_op.max_row
    for row in range(2, max_row + 1):
        arch = sheet_op.cell(row=row, column=3).value
        types = sheet_op.cell(row=row, column=2).value

        if arch is None:
            break
        elif arch.strip("\n") == "all" or sys_arch in arch.strip("\n"):
            cfg = sheet_op.cell(row=row, column=1).value.strip("\n")
            if "profile-sets" in types:
                expect_profile_lst.append(cfg)
            elif "path" in types:
                expect_path_lst.append(cfg)
        else:
            continue

    cmd1 = r"find /usr/share/pulseaudio/alsa-mixer/profile-sets/|awk -F '/' '{print $7}'"
    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    tmp = p001.stdout.read().replace("请输入密码", "").replace("验证成功", "")
    acture_profile_lst = tmp.strip().split("\n")

    cmd2 = r"find /usr/share/pulseaudio/alsa-mixer/paths/|awk -F '/' '{print $7}'"
    p002 = subprocess.Popen(cmd2,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    tmp1 = p002.stdout.read().replace("请输入密码", "").replace("验证成功", "")
    acture_path_lst = tmp1.strip().split("\n")

    logging.debug(acture_profile_lst)
    logging.debug(expect_profile_lst)
    logging.debug(acture_path_lst)
    logging.debug(expect_path_lst)

    # if len(acture_user_lst) == len(expect_user_lst):
    if len(list(set(acture_profile_lst) -
                set(expect_profile_lst))) == 0 and len(
                    list(set(expect_profile_lst) -
                         set(acture_profile_lst))) == 0 and len(
                             list(set(acture_path_lst) - set(expect_path_lst))
                         ) == 0 and len(
                             list(set(expect_path_lst) -
                                  set(acture_path_lst))) == 0:
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        logging.error("实际多了" +
                      str(set(acture_profile_lst) - set(expect_profile_lst)))
        logging.error("预期少了" +
                      str(set(expect_profile_lst) - set(acture_profile_lst)))
        logging.error("实际多了" +
                      str(set(acture_path_lst) - set(expect_path_lst)))
        logging.error("预期少了" +
                      str(set(expect_path_lst) - set(acture_path_lst)))
        assert False
