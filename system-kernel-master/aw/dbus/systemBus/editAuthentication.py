# -*- coding: utf-8 -*-
import os
import re
import dbus
import time
import pexpect
import logging
import threading
import subprocess

from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

DBusGMainLoop(set_as_default=True)

from frame import constant
from frame.decorator import checkword
from subprocess import getstatusoutput


def system_bus(dbus_name='com.deepin.daemon.Grub2', dbus_path='/com/deepin/daemon/Grub2/EditAuthentication',
               iface_name='com.deepin.daemon.Grub2.EditAuthentication'):
    system_bus = dbus.SystemBus()
    system_obj = system_bus.get_object(dbus_name, dbus_path)
    property_obj = dbus.Interface(system_obj, dbus_interface=iface_name)
    return property_obj


def cmd_input(passwd, dbus_name='com.deepin.daemon.Grub2', dbus_path='/com/deepin/daemon/Grub2/EditAuthentication',
              dbus_iface=None):
    cmd = f'echo {passwd} | sudo -S dbus-send --system --print-reply  --dest={dbus_name} {dbus_path} {dbus_iface}'
    time.sleep(1)
    logging.info(cmd)

    (status, output) = getstatusoutput(cmd)
    if status == 0:
        logging.info("命令执行成功")
    else:
        logging.info("命令执行失败")


@checkword
def disable(passwd, username):
    """
    关闭用户的Grub认证
    :param username:string 用户名
    :return: True or False
    """
    time.sleep(1)
    property_obj = system_bus()
    cmd_input(passwd, dbus_path='/com/deepin/daemon/Grub2',
              dbus_iface='com.deepin.daemon.Grub2.EditAuthentication.Disable string:{}'.format(username))
    logging.info("关闭用户Grub2认证")
    return True


@checkword
def enable(passwd, username, password):
    """
    开启用户的Grub认证
    :param passwd:string 被测系统密码
    :param username:string 测试用户名
    :param password:string 测试账户密码
    :return: True or False
    """
    time.sleep(1)
    property_obj = system_bus()
    cmd_input(passwd, dbus_path='/com/deepin/daemon/Grub2',
              dbus_iface='com.deepin.daemon.Grub2.EditAuthentication.Enable string:{} string{}'.format(username,
                                                                                                        password))
    logging.info("开启用户免grub2认证")
    return True


@checkword
def getEnabledUsers():
    """
    已开启Grub认证的用户列表
    :return: True or False
    """
    time.sleep(1)
    property_obj = system_bus(iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Grub2', 'EnbaledUsers')
    logging.info(dbus_out)
    if isinstance(dbus_out, dbus.Array):
        logging.info("获取已开启Grub认证的用户列表")
        return True
    else:
        logging.info("获取已开启Grub认证的用户列表失败")
        return False


def get_EnabledUsers():
    """
    已开启Grub认证的用户列表
    :return: Array,已开启grub2认证的用户列表
    """
    time.sleep(1)
    property_obj = system_bus(iface_name='org.freedesktop.DBus.Properties')
    dbus_out = property_obj.Get('com.deepin.daemon.Grub2', 'EnbaledUsers')
    logging.info(dbus_out)
    return dbus_out


@checkword
def check_user_isEnabled(username, status):
    """
    检查用户的认证状态
    """
    if status == 'Enabled':
        user_list = get_EnabledUsers()
        if username in user_list:
            return True
        else:
            logging('检查用户开启grub2认证状态失败')
            return False
    if status == 'Disabled':
        user_list = get_EnabledUsers()
        if username not in user_list:
            return True
        else:
            logging('检查用户关闭grub2认证状态失败')
            return False
