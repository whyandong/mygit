# -*- coding: utf-8 -*-
# com.deepin.dde.Launcher相关
import os
import time
import logging

import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.dde.Launcher'
DBUS_PATH = '/com/deepin/dde/Launcher'
IFACE_NAME = 'com.deepin.dde.Launcher'


# ===========================
#         功能函数
# ===========================
def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


@checkword
def exit():
    """
    退出启动器
    :param 无
    :return:True
    """
    time.sleep(1)
    interface = dbus_interface()
    interface.Exit()
    return True


@checkword
def hide():
    """
    隐藏启动器
    :param 无
    :return:True
    """
    time.sleep(1)
    interface = dbus_interface()
    interface.Hide()
    return True


@checkword
def isVisible():
    """
    启动器是否可见
    :param 无
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.IsVisible()
    logging.info(f'启动器状态值为{result}')
    if isinstance(result, dbus.Boolean):

        return True
    else:
        return False


@checkword
def show():
    """
    显示启动器
    :param 无
    :return:True
    """
    time.sleep(1)
    interface = dbus_interface()
    interface.Show()
    return True


@checkword
def showByMode(in0):
    """
    启动器显示方式
    :param 无
    :return:True
    """
    interface = dbus_interface()
    interface.ShowByMode(in0)
    return True


@checkword
def toggle():
    """
    切换启动器显示状态
    :param 无
    :return:True
    """
    interface = dbus_interface()
    interface.Toggle()
    return True


@checkword
def uninstallApp(appKey):
    """
    卸载app
    :param 无
    :return:True
    """
    interface = dbus_interface()
    interface.UninstallApp(appKey)
    return True


'================属性方法==================='


def visible():
    result = get_properties_value(dbus.String('Visible'))
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        return True
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False


if __name__ == '__main__':
    visible()
