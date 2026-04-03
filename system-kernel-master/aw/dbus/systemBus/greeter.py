# -*- coding: utf-8 -*-
import logging
import dbus
import time

from frame.decorator import checkword
from aw.dbus.systemBus import systemCommon
from aw.dbus.dbus_common import get_system_dbus_interface

DBUS_NAME = 'com.deepin.daemon.Greeter'
DBUS_PATH = '/com/deepin/daemon/Greeter'
IFACE_NAME = 'com.deepin.daemon.Greeter'


def dbus_interface():
    return get_system_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_system_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


@checkword
def updateGreeterQtTheme(fd):
    """
    更新开机Qt主题配置信息
    :param fd:Int32
    :return:Boolean
    """
    interface = dbus_interface()
    interface.UpdateGreeterQtTheme(fd)
    return True
