#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:    601050
# @Test Description: 使用sslscan检查tls安全协议版本是否支持tls1.3
# @Test Condition:
# @Test Step:   1.使用sslscan检查TLS协议版本
# @Test command:    sslscan --tlsall 127.0.0.1 | grep 'TLSv1.3' | grep 'enabled'
# @Test expect Result:   1.系统支持TLS1.3协议版本
# @Test Remark:
# @Author:  夏曙_ut000220
# @Date: 2022/6/8
# *****************************************************
import sys
import os
import pytest
import logging
import subprocess

from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enable stage !")
    os.system("echo 1 | sudo -S  apt install  apache2 -y")
    os.system(
        "echo 1 | sudo -S cp /etc/apache2/mods-available/ssl.load /etc/apache2/mods-enabled"
    )
    os.system(
        "echo 1 | sudo -S cp /etc/apache2/sites-available/default-ssl.conf /etc/apache2/mods-enabled/ssl.conf"
    )
    os.system("cd ./configs;unzip sslscan.zip -d ~/")
    os.system("cd ~/sslscan;echo 1 | sudo -S make;echo 1 | sudo -S make install")
    os.system("echo 1|sudo -S systemctl restart apache2.service")
    yield
    os.system("cd ~;rm -rf  sslscan")
    os.system("echo 1 | sudo -S apt remove apache2 -y --purge")
    logging.info("this is env disable stage !")


def test_tls_sslscan_601050():
    logging.info("step1:使用sslscan检查TLS协议版本")
    cmd1 = r"sslscan --tlsall 127.0.0.1 | grep 'TLSv1.3' | grep 'enabled'"
    p001 = subprocess.Popen(cmd1,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
    res1 = p001.stdout.read().strip()
    logging.info("res1:" + res1)

    if res1.strip() != "":
        logging.info(res1)
        assert True
    else:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        logging.error("系统不支持TLS1.3协议版本，不符合安全基线规范")
        logging.debug(res1)
        assert False
