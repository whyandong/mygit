#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          809303
# @Test Description:      wget连接非国密https网页
# @Test Condition:
# @Test Step:             1.使用TLSv1_1 协议连接百度网站 2. 使用国密GMTLSv1_1协议连接百度网站
# @Test expect Result:    1.正常连接 2.错误连接，提示错误信息
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
    execute_command("echo 1 | sudo -S rm -rf index.html")
    logging.info("this is env disable stage !")


def test_wget_nogm_https_287633():
    logging.info("step1:使用TLSv1_1 协议连接百度网站")
    curl_connect1 = execute_command(
        "wget --verbose --secure-protocol TLSv1_1 https://www.baidu.com")

    logging.info(curl_connect1)

    if '200 OK' in curl_connect1:
        assert True
    else:
        logging.error("wget连接无CA证书国密网页有误,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False

    logging.info("step2:使用国密GMTLSv1_1协议连接百度网站")

    curl_connect2 = execute_command(
        "wget --verbose --secure-protocol GMTLSv1_1 https://www.baidu.com")

    logging.info(curl_connect2)

    if 'OpenSSL: error' in curl_connect2:
        assert True
    else:
        logging.error("step2:wget连接无CA证书国密网页有误,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
