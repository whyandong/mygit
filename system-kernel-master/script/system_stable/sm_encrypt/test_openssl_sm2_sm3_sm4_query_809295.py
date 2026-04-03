#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          809295
# @Test Description:      openssl国密算法支持查询
# @Test Condition:
# @Test Step:           1.sm2算法支持查询 2.sm3算法支持查询 3.sm4算法支持查询
# @Test expect Result:  1.支持sm2算法 2.支持sm3算法 3.支持sm4算法
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


def test_openssl_sm2_sm3_sm4_query_288880():
    logging.info("step1:sm2算法支持查询")
    cmd1 = "openssl ecparam -list_curves |grep SM2|awk -F ':' '{print $1}'".strip(
    )

    sm2_check = execute_command(cmd1)

    if "SM2" in sm2_check:
        logging.info("支持sm2算法! ")
        assert True
    else:
        logging.error("不支持sm2算法, 请检查 !")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False

    cmd2 = "openssl list --digest-commands"

    sm3_check = execute_command(cmd2)

    logging.info("step2:sm3算法支持查询")

    if "sm3" in sm3_check:
        logging.info("支持sm3算法! ")
        assert True
    else:
        logging.error("不支持sm3算法, 请检查 !")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False

    cmd3 = "openssl enc -ciphers |grep sm4"

    sm4_check = execute_command(cmd3)

    logging.info("step3:sm4算法支持查询")

    if "sm4" in sm4_check:
        logging.info("支持sm4算法! ")
        assert True
    else:
        logging.error("不支持sm4算法, 请检查 !")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
