#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          809315
# @Test Description:      openssl使用国密sm2算法生成公钥和私钥
# @Test Condition:        已存在内容为abc的测试文件test.txt
# @Test Step:           1.通过sm2算法生成私钥 2.生成对应的公钥 3.将私钥转换成PKCS#8格式  4.使用公钥加密文件 5.使用私钥解密文件 6.对比test.txt和de_test.txt
# @Test expect Result:  1.解密的de_test.txt文件和初始文件test.txt无差异
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
        "echo '1' |sudo -S rm -rf test.txt de_test.txt pri.key priv_pkcs8.key pub.key en_test.bin"
    )


def test_openssl_sm2_create_pri_pub_key_285349():
    logging.info("step1:通过sm2算法生成私钥")
    cmd1 = "openssl ecparam -genkey -name SM2 -out pri.key"
    pri_key = execute_command(cmd1)
    logging.info("step2:生成对应的公钥")
    cmd2 = "openssl ec -in pri.key -pubout -out pub.key"
    pub_key = execute_command(cmd2)
    logging.info("step3:将私钥转换成PKCS#8格式")
    cmd3 = "openssl pkcs8 -topk8 -inform PEM -in pri.key -outform PEM -out priv_pkcs8.key -nocrypt"
    PKCS_file = execute_command(cmd3)
    logging.info("step4:使用公钥加密文件")
    cmd4 = "openssl pkeyutl -encrypt -inkey pub.key -pubin -in test.txt -out en_test.bin"
    encrypt_file = execute_command(cmd4)
    cmd5 = "openssl pkeyutl -decrypt -inkey priv_pkcs8.key -in en_test.bin -out de_test.txt"
    logging.info("step5:使用私钥解密文件")
    decrypt_file = execute_command(cmd5)

    logging.info("对比test.txt和de_test.txt")
    diff1 = execute_command("diff test.txt de_test.txt")

    if len(diff1) == 0:
        assert True
    else:
        logging.info("生成公钥或私钥出错，请检查")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
