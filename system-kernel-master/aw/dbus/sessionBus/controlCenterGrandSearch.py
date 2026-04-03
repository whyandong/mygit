# -*- coding: utf-8 -*-
# com.deepin.dde.controlcenter相关
import os
import time
import logging

import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.dde.ControlCenter'
DBUS_PATH = '/com/deepin/dde/ControlCenter'
IFACE_NAME = 'com.deepin.dde.ControlCenter.GrandSearch'


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
def search(json):
    """
    匹配搜索结果
    :param json json数据
    :return:Boolearn
    """
    interface = dbus_interface()
    reslut = interface.Search(json)
    logging.info(reslut)
    if isinstance(reslut,dbus.String):
        return True
    else:
        logging.info(f'搜索失败，返回值类型不匹配，返回类型为{type(reslut)}')


@checkword
def action(json):
    """
    执行搜索
    :param json json数据类型
    :return:Boolearn
    """
    interface = dbus_interface()
    reslut = interface.Action(json)
    logging.info(reslut)
    if isinstance(reslut,dbus.Boolean):
        return True
    else:
        logging.info(f'搜索失败，返回值类型不匹配，返回类型为{type(reslut)}')

@checkword
def stop(json):
    """
    停止搜索
    :param json json数据类型
    :return:Boolearn
    """
    interface = dbus_interface()
    reslut = interface.Stop(json)
    logging.info(reslut)
    if isinstance(reslut,dbus.Boolean):
        return True
    else:
        logging.info(f'搜索失败，返回值类型不匹配，返回类型为{type(reslut)}')

if __name__ == '__main__':
    stop('network:"VPN"')
