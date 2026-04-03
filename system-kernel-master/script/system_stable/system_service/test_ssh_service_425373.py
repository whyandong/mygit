#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ****************************************************
# @Test Case ID:          425373
# @Test Description:      ssh服务默认禁用检查与启用功能验证
# @Test Condition:        更新仓库并等待2s
# @Test Step:             1.检查ssh服务是否未关闭状态 2.安装openssh-server  3.重新启动ssh服务 4.检查ssh服务是否为active 5.ssh连接本机地址127.0.0.1
# @Test expect Result:    1.正常安装openssh-server 2.正常重启ssh服务 3.ssh服务为active
# @Test Remark:
# @Author:  杨浪_ut001228
# *****************************************************
import sys
import pytest
import logging
import os
import paramiko
import subprocess

from frame.common import system_kernel_log_cap


@pytest.fixture(scope="function", autouse=True)
def env_enable_disable():
    logging.info("this is env enablle stage !")
    yield
    logging.info("this is env disable stage !")
    os.system("echo 1|sudo -S systemctl stop ssh")


def get_ssh_service_status():
    cmd = r"echo 1|sudo -S systemctl status  ssh |grep Active | awk -F ':' '{print $ 2}'"
    p0 = subprocess.Popen(cmd,
                          shell=True,
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          encoding='utf-8')
    status = p0.stdout.readline().replace("验证成功", '').strip("\n")
    return status


def test_ssh_service_425373():
    logging.info('step1:检查ssh服务是否未关闭状态')
    ssh_status = get_ssh_service_status()
    logging.debug(ssh_status)
    if "inactive" in ssh_status:
        logging.info("ssh服务默认为关闭状态")
        assert True
    else:
        logging.info("ssh服务默认不为关闭状态,请检查ssh服务是否被手动开启")
        assert False

    logging.info('step2:可以正常启动ssh服务')
    os.system("echo 1|sudo -S systemctl start ssh")
    logging.info('step3:检查ssh服务是否为active')
    ssh_status = get_ssh_service_status()
    logging.debug(ssh_status)
    if "inactive" not in ssh_status and "active" in ssh_status:
        assert True
    else:
        logging.error("step2开启ssh服务失败, 请检查系统! ")
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False

    logging.info('step4:检查ssh连接本机地址127.0.0.1')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='127.0.0.1', port=22, username='uos', password='1')
    sys.stdin, sys.stdout, sys.stderr = ssh.exec_command('ls')
    result = sys.stdout.read().decode('utf-8')
    ssh.close()

    if 'Desktop' in result:
        logging.debug(result)
        assert True
    else:
        logging.error(result)
        logging.error('ssh连接本机地址失败, 请检查!')
        tsc_name = sys._getframe().f_code.co_name
        system_kernel_log_cap(tsc_name)
        assert False
