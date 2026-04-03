#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:         169829
# @Test Description:     OsBuild信息校对
# @Test Condition:    OS Build：（按系统构建信息和周期）
# @【ABCDE.xyz】
# @解释：
# @A：系统
# @【1：20】 【2：23】 【3：25】 【4：26】 【5：29】 【6：30】
# @B：系统类型
# @【1：桌面】【2：服务器】【3：专用设备】
# @C：预留（默认0）
# @0：标准镜像
# @1: Alpha 版本 (第一个内测版本，存在一定bug，内部测试使用，内网仓库)
# @2: Beta 版本（公测版本，对生态厂商和商业项目升级和适配测试使用，存在少量bug，提供ppa仓库）
# @3: RC 版本（预发布版本，质量/性能与正式发行版相同，代码冻结，发布前验证，内网仓库）
# @4: 性能优化送测版（性能调优版，性能调优参数不出现在当期主线发布中，为前端性能pk使用，独立分支仓库，不持续维护和升级）
# @D：版本名称（0-9, A-Z）
# @B=1时， D=【1：专业版】【2：个人版】【3：社区版】【4：军用版】
# @B=2时,D=【1：企业版】【2：行业版】【3：欧拉版】【4：军用版】
# @B=3时,D=【1：企业版】
# @E：架构信息（使用一个字节的二进制位，从低位到高位）
# @【】【】【】【】【amd64】【arm64】【mips64】【sw64】【lonngarch】
# @0000 0001：1（SW64）
# @0000 0010：2（MIPS64）
# @0000 0011：3（LONNGARCH）
# @0000 0100：4（ARM64）
# @0000 1000：8（amd64）
# @xyz：为系统镜像批次号，首次构建批次号为100，按时间顺序（不可回退）从100-999递增
# @Test Step:  cat /etc/os-version查看OsBuild字段与当前版本信息、平台信息是否匹配
# @Test expect Result: OsBuild字段与当前版本信息、平台信息一致
# @Test Remark:
# @Author:  ut002037
# *****************************************************
import sys

import pytest
import logging
from frame.common import get_platform_arch
from frame.common import system_kernel_log_cap

MajorVersion = {
    '1': '20',
    '2': '23',
    '3': '25',
    '4': '26',
    '5': '29',
    '6': '30'
}
ProductType = {'1': '桌面', '2': '服务器', '3': '专用设备'}
ImageType = {
    '0': '标准镜像',
    '1': 'Alpha镜像',
    '2': 'Beta版本',
    '3': 'RC版本',
    '4': '性能优化送测版本'
}
EditionName1 = {'1': '专业版', '2': '个人版', '3': '社区版', '4': '军用版'}
EditionName2 = {'1': '企业版', '2': '行业版', '3': '欧拉版', '4': '军用版'}
EditionName3 = {'1': '企业版'}
Sys_Arch = {
    '1': 'SW64',
    '2': 'MIPs64',
    '3': "loongarch",
    '4': 'ARM64',
    '8': 'amd64'
}


def load_cfg2dic(filepath, cfg):
    with open(filepath) as f:
        for line in f.readlines():
            if "=" not in line:
                continue
            else:
                tmp = line.strip(" \n").split("=")
                cfg[tmp[0]] = tmp[1]


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_check_osbuild_169829():
    system_info = {}
    key_word = [
        "ProductType[zh_CN]", "EditionName[zh_CN]", "MajorVersion", "OsBuild"
    ]
    load_cfg2dic("/etc/os-version", system_info)
    major_version = MajorVersion[system_info[key_word[3]][0]]
    product_type = ProductType[system_info[key_word[3]][1]]
    if system_info[key_word[3]][1] == "1":
        EditionName = EditionName1
    elif system_info[key_word[3]][1] == "2":
        EditionName = EditionName2
    elif system_info[key_word[3]][1] == "3":
        EditionName = EditionName3

    edition_name = EditionName[system_info[key_word[3]][3]]
    sys_arch = Sys_Arch[system_info[key_word[3]][4]].upper()

    acture_arch = get_platform_arch().upper()
    acture_major_version = system_info[key_word[2]]
    acture_product_type = system_info[key_word[0]]
    acture_edition_name = system_info[key_word[1]]

    if edition_name == acture_edition_name and acture_arch in sys_arch and acture_major_version == major_version and acture_product_type == product_type:
        assert True
    else:
        logging.debug(acture_arch)
        logging.debug(acture_major_version)
        logging.debug(acture_product_type)
        logging.debug(acture_edition_name)
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
