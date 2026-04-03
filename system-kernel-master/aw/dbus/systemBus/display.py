# -*- coding: utf-8 -*-
import logging
import dbus

from aw.dbus.dbus_common import get_system_dbus_interface
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.system.Display'
DBUS_PATH = '/com/deepin/system/Display'
IFACE_NAME = 'com.deepin.system.Display'


# 程序：/usr/lib/deepin-daemon/dde-system-daemon
# 功能：提供设置和获取系统级显示配置文件


def dbus_interface():
    return get_system_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


@checkword
def getConfig():
    """
    获取系统级显示配置
    :return:string
    """
    interface = dbus_interface()
    result = interface.GetConfig()
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info("返回数据类型为dbus.String正常")
        return True
    else:
        logging.info(f'返回数据类型为dbus.String异常,返回值类型为{type(result)}')
        return False


def get_Config():
    """
    获取系统级显示配置
    :return: string
    """
    interface = dbus_interface()
    result = interface.GetConfig()
    print(result)
    if isinstance(result, dbus.String):
        logging.info("返回数据类型为dbus.String正常")
        return result
    else:
        logging.info(f'返回数据类型为dbus.String异常,返回值类型为{type(result)}')
        return False

@checkword
def setConfig(value):
    """
    设置系统级显示配置文件
    ：param:String
    :return:Boolean
    """
    interface = dbus_interface()
    interface.SetConfig(value)
    return True

@checkword
def checkConfig(value):
    """
    param: value 配置文件信息
    return：Boolean
    """
    result = get_Config()
    if result == value:
        logging.info('检查点通过')
        return True
    else:
        logging.info(f'设置的值为{value},当前获取到的值为{result}')
        return False
