# -*- coding: utf-8 -*-
# com.deepin.dde.Launcher相关
import os
import time
import logging

import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.dde.MemoryWarningDialog'
DBUS_PATH = '/com/deepin/dde/MemoryWarningDialog'
IFACE_NAME = 'com.deepin.dde.MemoryWarningDialog'


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
def show(launcherinfo):
    """
    显示内存警告信息
    :param 无
    :return:True
    """
    interface = dbus_interface()
    interface.Show(launcherinfo)
    return True


@checkword
def hide():
    """
    隐藏内存警告信息
    :param 无
    :return:True
    """
    interface = dbus_interface()
    interface.Hide()
    return True
