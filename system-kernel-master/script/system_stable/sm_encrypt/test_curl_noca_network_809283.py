#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          809283
# @Test Description:      curl连接无CA证书国密网页
# @Test Condition:
# @Test Step:             1.curl连接无CA证书国密网页
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


def test_curl_noca_network_290776():
    logging.info("step1:curl连接无CA证书国密网页")
    curl_connect = execute_command(
        "curl -l --gmtlsv1.1 https://sm2test.ovssl.cn:443")

    if 'failed' in curl_connect:
        assert True
    else:
        logging.error("curl连接无CA证书国密网页有误,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
