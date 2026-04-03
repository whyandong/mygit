#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          809301
# @Test Description:      curl连接非国密https网页
# @Test Condition:
# @Test Step:             1.使用TLSv1.2 协议连接百度网站 2. 使用国密GMTLSv1_1协议连接百度网站
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
    logging.info("this is env disable stage !")


def test_curl_nogm_https_287634():
    logging.info("step1:使用TLSv1.2 协议连接百度网站")
    curl_connect1 = execute_command("curl -v https://www.baidu.com")

    if 'HTTP/1.1 200 OK' in curl_connect1:
        assert True
    else:
        logging.error("curl连接无CA证书国密网页有误,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False

    logging.info("step2:使用国密GMTLSv1_1协议连接百度网站")
    curl_connect2 = execute_command(
        "curl -v --gmtlsv1.1 https://www.baidu.com")

    if 'GMTLSv1.1 (OUT), , Unknown' in curl_connect2:
        assert True
    else:
        logging.error("curl连接无CA证书国密网页有误,请检查！")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
