# -*- coding: utf-8 -*-
import os
import time
import logging

import dbus

from frame.decorator import checkword
from aw.dbus.systemBus import systemCommon

dbus_name = 'com.deepin.daemon.Timedated'
dbus_path = '/com/deepin/daemon/Timedated'
iface_name = 'com.deepin.daemon.Timedated'


@checkword
def setLocalRTC(passwd, enabled, fixsystem, message):
    """
    设置实时钟为本地时间或世界统一时间
    :param enabled:true为本地时间， false为世界统一时间
    :param fixsystem:true或false, 是否修正系统时间
    :param message:关于设置实时钟的认证信息
    :return:True or False
    """
    dbus_iface_method = f'com.deepin.daemon.Timedated.SetLocalRTC boolean:{enabled} boolean:{fixsystem} string:{message}'
    result = systemCommon.cmd_input(passwd, dbus_name, dbus_path, dbus_iface_method=dbus_iface_method)
    time.sleep(6)
    logging.info(result)
    if 'method' in result:
        logging.info(f'设置时钟为{enabled}成功，设置系统时间为{fixsystem}成功')
        return True
    else:
        logging.info("设置参数失败")
        return False


@checkword
def setLocalRTC2(passwd, enabled, fixsystem, message):
    """
    设置实时钟为本地时间或世界统一时间(通过sudo -S免输密码)
    :param passwd:用户密码
    :param enabled:true为本地时间， false为世界统一时间
    :param fixsystem:true或false, 是否修正系统时间
    :param message:关于设置实时钟的认证信息
    :return:True or False
    """
    cmd = f"echo {passwd} |sudo -S dbus-send --system --print-reply  --dest=com.deepin.daemon.Timedated /com/deepin/daemon/Timedated com.deepin.daemon.Timedated.SetLocalRTC boolean:{enabled} boolean:{fixsystem} string:{message}"
    logging.info(cmd)
    f = os.popen(cmd)
    result = f.read()
    logging.info(result)
    f.close()
    if 'method' in result:
        logging.info(f'设置时钟为{enabled}成功，设置系统时间为{fixsystem}成功')
        return True
    else:
        logging.info("设置参数失败")
        return False


@checkword
def setNTP(enabled, message):
    """
    设置系统时钟是否和网络时钟同步
    :param enabled:true为系统时钟和网络时钟同步， false为系统时钟和网络时钟不同步
    :param message:关于设置系统时钟的认证信息
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.SetNTP(dbus.Boolean(enabled), dbus.String(message))
    time.sleep(6)
    logging.info(result)
    if not result:
        logging.info(f'设置系统时钟和网络时钟状态为{enabled}成功')
        return True
    else:
        logging.info("设置参数失败")
        return False


@checkword
def setNTPServer(passwd, server, message):
    """
    设置网络时间协议服务器
    :param server:网络时间协议服务器
    :param message:关于设置网络时间服务器的认证信息
    :return:True or False
    """
    dbus_iface_method = f'com.deepin.daemon.Timedated.SetNTPServer string:{server} string:{message}'
    result = systemCommon.cmd_input(passwd, dbus_name, dbus_path, dbus_iface_method=dbus_iface_method)
    logging.info(result)
    if 'method' in result:
        logging.info('设置网络时间协议服务器成功')
        return True
    else:
        logging.info("设置网络时间协议服务器失败")
        return False


@checkword
def setTime(usec, relative, message):
    """
    设置当前时间和日期
    :param usec:自1970年1月1日零时起， 到当前时间的微秒数
    :param relative:是否关联
    :param message:关于设置当前时间和日期的认证信息
    :return:True or False
    :examlpe:1595487474000000,True,''
    """
    time.sleep(2)
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.SetTime(dbus.Int64(usec), dbus.Boolean(relative), dbus.String(message))
    logging.info(result)
    if not result:
        logging.info('设置当前时间和日期成功')
        return True
    else:
        logging.info("设置当前时间和日期失败")
        return False


@checkword
def setTimezone(passwd, timezone, message):
    """
    设置时间区域
    :param timezone: 所在时间区域(时间区域信息：/usr/share/zoneinfo/zone.tab)
    :param message:关于设置时间区域的认证信息
    :return:True or False
    """
    dbus_iface_method = f'com.deepin.daemon.Timedated.SetTimezone string:{timezone} string:{message}'
    result = systemCommon.cmd_input(passwd, dbus_name, dbus_path, dbus_iface_method=dbus_iface_method)
    logging.info(result)
    if 'method' in result:
        logging.info('设置时间区域成功')
        return True
    else:
        logging.info("设置时间区域失败")
        return False


@checkword
def getNTPServer():
    """
    网络时间协议服务器
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get('com.deepin.daemon.Timedated', 'NTPServer')
    logging.info(result)
    if result:
        logging.info('设置时间区域成功')
        return True
    else:
        logging.info("设置时间区域失败")
        return False
