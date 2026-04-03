#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
import subprocess
# ****************************************************
# @Test Case ID:          478362
# @Test Description:       蓝牙的运行参数用户自定义,可以通过配置文件设置是否去掉input插件
# @Test Condition:
# @Test Step:             1.创建配置文件 2.重启服务检查input插件是否去掉
# @Test expect Result:    1.正常创建配置文件  2.服务已去掉input插件
# @Test Remark:
# @Author:  杨浪_ut001228
# *****************************************************
import sys
import pytest
from frame.common import execute_command, system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    os.system("echo 1|sudo -S  rm -rf /usr/share/bluetooth")
    os.system("echo 1|sudo -S systemctl restart bluetooth.service")


def test_bluetooth_input_478362():
    logging.info("检查是否已加载蓝牙驱动")
    cmd = r"echo 1 |sudo -S lshw |grep bluetooth |awk -F ':' '{print$2}'"
    p = subprocess.Popen(cmd,
                         shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         encoding='utf-8')
    bluetooth_driver = p.stdout.read().replace("请输入密码", "").replace("验证成功", "")
    logging.debug(bluetooth_driver)

    if "bluetooth" in bluetooth_driver:
        os.system("cd ./configs/system;echo 1|sudo -S bash test_478362.sh")
        cmd = r'cat /usr/share/bluetooth/bluetoothd.conf'
        p = subprocess.Popen(cmd,
                             shell=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             encoding='utf-8')
        test_bluetooth = p.stdout.read().replace("请输入密码",
                                                 "").replace("验证成功", "")
        logging.debug(test_bluetooth)

        logging.info("step2:检查服务是否去掉input插件")
        os.system("echo 1|sudo -S systemctl restart bluetooth.service")
        servie_check = execute_command(
            "systemctl status bluetooth.service | grep '/usr/lib/bluetooth/bluetoothd --noplugin=input'"
        )
        logging.debug(servie_check)

        if 'input' in servie_check:
            assert True
        else:
            logging.error("服务未去掉input插件,请检查!")
            tsc_name = sys._getframe().f_code.co_name
            system_kernel_log_cap(tsc_name)
            assert False
    else:
        pytest.skip(msg="没有加载蓝牙驱动,跳过此用例!")
