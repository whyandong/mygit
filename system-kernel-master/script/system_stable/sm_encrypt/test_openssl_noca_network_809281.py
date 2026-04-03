#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          809281
# @Test Description:      openssl连接无CA证书国密网页
# @Test Condition:
# @Test Step:             1.openssl连接无CA证书国密网页
# @Test expect Result:    1.由于证书校验失败导致连接失败、
# @Test Remark:
# @Author:  杨浪_ut001228
# *****************************************************
import sys
import pytest
import logging


from frame.common import execute_command
from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_openssl_noca_network_290935():
    logging.info("step1:openssl连接无CA证书国密网页 ")
    openssl_connect = execute_command(
        "openssl s_client -msg -gmtls -connect sm2test.ovssl.cn:443")
    logging.info(openssl_connect)
    if 'verify error' in openssl_connect:
        assert True
    else:
        logging.error("openssl连接无CA证书国密网页 有误,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
