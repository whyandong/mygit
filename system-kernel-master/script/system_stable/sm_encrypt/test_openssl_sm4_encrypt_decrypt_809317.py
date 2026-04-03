#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          809317
# @Test Description:      openssl使用国密sm4算法进行对称加解密
# @Test Condition:        已存在内容为abc的测试文件test.txt
# @Test Step:           1.检查sm4加密算法的正确性 2.对test.txt文件使用sm4算法进行加密 3.使用sm4算法对encrypted_test.bin文件解密 4.对比test.txt和decode_test.txt
# @Test expect Result:  1.解密的decode_test.txt文件和初始文件test.txt无差异
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
    execute_command("echo '1' |sudo -S echo 'abc'>test.txt")
    yield
    execute_command(
        "echo '1' |sudo -S rm -rf test.txt decode_test.txt encrypted_test.bin")


def test_openssl_sm4_encrypt_decrypt_285241():
    logging.info("step1:检查sm4加密算法的正确性")
    cmd1 = "echo -e -n '\x01\x23\x45\x67\x89\xAB\xCD\xEF\xFE\xDC\xBA\x98\x76\x54\x32\x10' | openssl enc -sm4 -K 0123456789ABCDEFFEDCBA9876543210 -iv 00000000000000000000000000000000 -pbkdf2 -iter 1 -e -nosalt | xxd -a -l 16 -p"
    sm4_cal = execute_command(cmd1).strip()

    logging.info(sm4_cal)

    if "a80f931e8a2eb94a1dfed34e5a054e92" == sm4_cal:
        logging.info("sm4加解密正确! ")
        assert True
    else:
        logging.error("sm4加解密错误, 请检查 !")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False

    logging.info("step2:对test.txt文件使用sm4算法进行加密")

    cmd2 = "openssl enc -sm4 -in test.txt -out encrypted_test.bin -e -pass pass:123456"

    sm4_encrypt = execute_command(cmd2)

    logging.info("step3:使用sm4算法对encrypted_test.bin文件解密")

    cmd3 = "openssl enc -sm4 -in encrypted_test.bin -out decode_test.txt -d -pass pass:123456"

    sm4_decrypt = execute_command(cmd3)

    logging.info("step4:对比test.txt和deode_test.txt")

    diff1 = execute_command("diff test.txt decode_test.txt")

    if len(diff1) == 0:
        assert True
    else:
        logging.info("sm4加密或解密出错, 请检查")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
