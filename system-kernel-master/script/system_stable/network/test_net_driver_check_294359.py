#!/usr/bin/python3
# -*- coding: utf-8 -*-

# *****************************************************************************************************
# @Test Case ID:      294359
# @Test Description:  lsmod、rmmod、modprobe查看、卸载、加载网卡驱动测试
# @Test Condition:
# @Test Step:  1.ifconfig | awk -F ":" 'NR==1{print $1}' 获取当前使用的网络接口
# @            2.lshw -c network|grep driver|awk '{print $4}'|awk -F '=' '{print $2}'获取当前加载的驱动，ping百度确认网络状态
# @            3.rmmod 卸载当前网络驱动，检查网络接口是否存在，ping www.baidu.com不通
# @            4.modprobe 安装之前卸载的驱动，检查网络接口是否存在，ping www.baidu.com确认网络状态
# @Test expect Result:  1.网络服务状态正常 2.卸载驱动后，接口消失，网络ping不通 3.安装驱动后。网络恢复，接口恢复
# @Test Remark:
# @Author:  ut002037
# ******************************************************************************************************
import sys
import pytest
import logging
import subprocess
import time

from frame.common import execute_command
from frame.common import system_kernel_log_cap


def network_status_check():
    get_ping_count_cmd = r"ping www.baidu.com -c 5 2>/dev/null|grep received|awk '{print $4}'"
    p = subprocess.Popen(get_ping_count_cmd,
                         shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         encoding='utf-8')
    ping_cnt = p.stdout.read().strip()

    if ping_cnt == '':
        logging.debug("ping failed !")
        return False
    elif int(ping_cnt) <= 5 and int(ping_cnt) > 0:
        logging.debug(ping_cnt)
        return True
    else:
        logging.debug(ping_cnt)
        return False


def get_network_interface():
    get_interface_cmd = r"ifconfig | awk -F ':' 'NR==1{print $1}'"
    logging.info("使用命令ifconfig | awk -F ':' 'NR==1{print $1}'获取当前网络接口:")
    interface = execute_command(get_interface_cmd).strip()
    logging.debug(interface)
    return interface


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")


def test_net_driver_check_294359():
    ret = True
    logging.info("获取正常开机时默认的网络接口：")
    default_interface = get_network_interface()
    logging.info(default_interface)

    logging.info(
        "使用命令echo 1 | sudo -S lshw -c network|grep driver|awk '{print $4}'|awk -F '=' '{print $2}'获取当前驱动:"
    )
    get_driver_cmd = "echo 1|sudo -S lshw -c network|grep 'driver'|awk '{print $4}'|awk -F '=' '{print $2}'"
    p = subprocess.Popen(get_driver_cmd,
                         shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         encoding='utf-8')
    driver = p.stdout.read().strip()
    logging.info(driver)

    if network_status_check():
        ret = ret and True
    else:
        logging.error('请检查驱动是否加载正常或者网络是否需要认证或者网线是否连接好！')
        ret = ret and False
    assert ret

    rmv_driver = 'echo 1 | sudo -S rmmod ' + driver
    rmmod_status = execute_command(rmv_driver)
    time.sleep(2)
    if rmmod_status != '':
        ret = ret and False
        logging.error("rmmod移除网卡驱动失败! ")
    else:
        logging.info("rmmod移除网卡驱动成功")
        ret = ret and True

    logging.info("获取驱动卸载后的当前网络接口:")
    cur_interface = get_network_interface()
    if cur_interface == default_interface:
        ret = ret and False
        logging.error("网卡驱动已卸载但网络接口还存在，请检查系统是否异常！")
    else:
        logging.debug('网卡驱动已经卸载')
        ret = ret and True

    modprobe_driver = 'echo 1 | sudo -S modprobe ' + driver
    modprobe_status = execute_command(modprobe_driver)
    time.sleep(60)
    if modprobe_status != '':
        ret = ret and False
        logging.error("modprobe安装网卡驱动失败! ")
    else:
        ret = ret and True
        logging.info("modprobe安装网卡驱动成功!")

    logging.info("获取网络驱动重新加载后的网络接口名称！")
    cur_interface1 = get_network_interface()
    logging.info(cur_interface1)
    if cur_interface1 != default_interface:
        ret = ret and False
        logging.error("网卡驱动已安装但加载的网络接口与卸载前不一致，请检查系统是否异常！")
    else:
        ret = ret and True

    if network_status_check():
        ret = ret and True
        logging.info("驱动已经安装成功, 网络接口能够正常up,网络连接良好！")
    else:
        logging.error('驱动已经安装成功，但网络连接不通，请检查系统是否异常!')
        ret = ret and False

    if not ret:
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
    assert ret
