# -*- coding: utf-8 -*-

import time
import logging
import pexpect
import subprocess
from subprocess import getstatusoutput

import dbus


def system_bus(dbus_name=None, dbus_path=None,
               iface_name=None):
    system_bus = dbus.SystemBus()
    system_obj = system_bus.get_object(dbus_name, dbus_path)
    property_obj = dbus.Interface(system_obj, dbus_interface=iface_name)
    return property_obj


def excute_cmd(cmd):
    """
    执行cmd命令
    :param cmd:输入的命令
    :return:string
    """
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, encoding='utf-8')

    outMsg = p.stdout.read()
    errMsg = p.stderr.read()
    if errMsg:
        return errMsg
    else:
        return outMsg


def cmd_input(passwd, dbus_name=None, dbus_path=None, dbus_iface_method=None):
    """
    dbus-send模式进行接口测试，sudo输入密码
    @param passwd: 密码
    @param dbus_name: 接口名
    @param dbus_path: 接口路径
    @param dbus_iface_method: 接口传入对应的方法和参数
    @return: string
    """
    #cmd = 'sudo dbus-send --system --print-reply  --dest={} {} {}'.format(dbus_name, dbus_path, dbus_iface_method)
    cmd = f'echo {passwd} | sudo -S dbus-send --system --print-reply  --dest={dbus_name} {dbus_path} {dbus_iface_method}'
    logging.info(cmd)
    time.sleep(1)
    (status, output) = getstatusoutput(cmd)
    if status == 0:
        logging.info("命令执行成功")
    else:
        logging.info("命令执行失败")
    # ret = pexpect.spawn(cmd)
    # i = ret.expect(['密码', pexpect.EOF, pexpect.TIMEOUT], timeout=10)
    # if i == 0:
    #     ret.sendline(passwd)
    #     result = ret.read().decode(encoding="utf-8")
    # else:
    #     b_content = ret.before
    #     result = str(b_content, encoding="utf-8", errors='ignore')
    #
    # return result.strip()
