#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import logging
import os

# ****************************************************
# @Test Case ID:      173127
# @Test Description:   /etc/apt/apt.conf.d/目录下99lastore.conf和99lastore-token.conf配置文件检查
# @Test Condition:
# @Test Step:
# 1.执行cat /etc/apt/apt.conf.d/99lastore.conf,检查配置
# 2. 执行cat /etc/apt/apt.conf.d/99lastore-token.conf，检查配置
# @Test expect Result:
# 1. 99lastore.conf配置文件有如下参数：
# Acquire::SmartMirrors::DomainList:: "deepin.com";
# Acquire::SmartMirrors::DomainList:: "deepin.org";
# Acquire::SmartMirrors::DomainList:: "uniontech.com";
# Acquire::SmartMirrors::DomainList:: "chinauos.com";
# 2. 99lastore-token.conf配置文件有如下参数：
# 版本信息v=XXXXX与与/etc/os-version中MajorVersion.MinorVersion.OsBuild进行对比一致
# @Test Remark:
# @Author:  夏曙_ut000220
# *****************************************************
import pytest
from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_check_apt_lable_173127():
    lastore_conf_base = [
        'Acquire::SmartMirrors::DomainList:: "deepin.com";',
        'Acquire::SmartMirrors::DomainList:: "deepin.org";',
        'Acquire::SmartMirrors::DomainList:: "uniontech.com";',
        'Acquire::SmartMirrors::DomainList:: "chinauos.com";'
    ]
    lastore_conf = os.popen(
        "cat /etc/apt/apt.conf.d/99lastore.conf").read().split("\n")
    logging.info(lastore_conf)
    logging.info(
        "step:检查/etc/apt/apt.conf.d/99lastore.conf和/etc/apt/apt.conf.d/99lastore-token.conf配置文件"
    )
    lastore_conf_err = [s for s in lastore_conf_base if s not in lastore_conf]

    MajorVersion = os.popen(
        "cat /etc/os-version | grep MajorVersion | awk -F= '{print $2}'").read(
        ).strip("\n")
    MinorVersion = os.popen(
        "cat /etc/os-version | grep MinorVersion | awk -F= '{print $2}'").read(
        ).strip("\n")
    OsBuild = os.popen(
        "cat /etc/os-version | grep OsBuild | awk -F= '{print $2}'").read(
        ).strip("\n")
    v_base = MajorVersion + '.' + MinorVersion + '.' + OsBuild
    lastore_v = os.popen(
        "cat /etc/apt/apt.conf.d/99lastore-token.conf | awk -F ';' '{print $4}' | awk -F= '{print $2}'"
    ).read().strip("\n")

    if lastore_conf_err == [] and lastore_v == v_base:
        assert True
    else:
        if lastore_conf_err != []:
            logging.error("/etc/apt/apt.conf.d/99lastore.conf配置错误,如下配置比较失败：")
            logging.error(lastore_conf_err)
        if lastore_v != v_base:
            logging.error(
                "/etc/apt/apt.conf.d/99lastore-token.conf版本信息错误,请检查！")
            logging.error("99lastore-token.conf版本信息:" + lastore_v)
            logging.error("os-version版本号:" + v_base)
            tsc_name = sys._getframe().f_code.co_name
            system_kernel_log_cap(tsc_name)
            assert False
