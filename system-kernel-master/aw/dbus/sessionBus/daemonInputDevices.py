# -*- coding: utf-8 -*-
import logging

import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.daemon.InputDevices'
DBUS_PATH = '/com/deepin/daemon/InputDevices'
IFACE_NAME = 'com.deepin.daemon.InputDevices'


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


@checkword
def infos():
    """
    InfoStruct[] Infos (read)

    type InfoStruct struct {
      string InterfaceName,
      string DeviceType
    }
    全部输入设备的接口
    字段含义:
            InterfaceName : 设备的DBus接口名
            DeviceType : 设备的类型
    :return: True or False
    """
    result = get_properties_value('Infos')
    if isinstance(result, dbus.Array):
        for info in result:
            if isinstance(info, dbus.Struct):
                logging.info(f"InterfaceName: {info[0]}")
                logging.info(f"DeviceType: {info[1]}")
            else:
                logging.info(f'类型错误：{type(info)}')
                return False
        else:
            return True

    else:
        return False


@checkword
def wheelSpeed():
    """
    uint32 WheelSpeed (readwrite)
    鼠标滚轮的速度
    :return: True or False
    """
    result = get_properties_value('WheelSpeed')
    if isinstance(result, dbus.UInt32):
        if dbus.UInt32(1) <= result < dbus.UInt32(10):
            logging.info(f"鼠标滚轮的速度: {result}")
            return True
        else:
            logging.info(f"读取到的鼠标滚轮的速度: {result}，不在预设值1-10之间")
            return False
    else:
        return False
