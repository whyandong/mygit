# -*- coding: utf-8 -*-
import logging

import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.daemon.SystemInfo'
DBUS_PATH = '/com/deepin/daemon/SystemInfo'
IFACE_NAME = 'com.deepin.daemon.SystemInfo'


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


@checkword
def cpuMaxMHz():
    """
    Double CPUMaxMHz (read)
    cpu的频率
    :return: True or False
    """
    result = get_properties_value('CPUMaxMHz')
    if isinstance(result, dbus.Double):
        logging.info(f"CPUMaxMHz: {result}")
        return True
    else:
        return False


@checkword
def systemType():
    """
    Int64 SystemType (read)
    系统的类型: 32/64位
    :return: True or False
    """
    result = get_properties_value('SystemType')
    if isinstance(result, dbus.Int64):
        logging.info(f"SystemType: {result}")
        return True
    else:
        return False


@checkword
def distroDesc():
    """
    String DistroDesc (read)
    发行说明
    :return: True or False
    """
    result = get_properties_value('DistroDesc')
    if isinstance(result, dbus.String):
        logging.info(f"DistroDesc: {result}")
        return True
    else:
        return False


@checkword
def distroID():
    """
    String DistroID (read)
    发行编号
    :return: True or False
    """
    result = get_properties_value('DistroID')
    if isinstance(result, dbus.String):
        logging.info(f"DistroID: {result}")
        return True
    else:
        return False


@checkword
def distroVer():
    """
    String DistroVer (read)
    发行版本
    :return: True or False
    """
    result = get_properties_value('DistroVer')
    if isinstance(result, dbus.String):
        logging.info(f"DistroVer: {result}")
        return True
    else:
        return False


@checkword
def processor():
    """
    String Processor (read)
    CPU信息
    :return: True or False
    """
    result = get_properties_value('Processor')
    if isinstance(result, dbus.String):
        logging.info(f"Processor: {result}")
        return True
    else:
        return False


@checkword
def version():
    """
    String Version (read)
    当前系统版本, 例如: "2015 Desktop"
    :return: True or False
    """
    result = get_properties_value('Version')
    if isinstance(result, dbus.String):
        logging.info(f"Version: {result}")
        return True
    else:
        return False


@checkword
def diskCap():
    """
    UInt64 DiskCap (read)
    磁盘容量
    :return: True or False
    """
    result = get_properties_value('DiskCap')
    if isinstance(result, dbus.UInt64):
        logging.info(f"DiskCap: {result}")
        return True
    else:
        return False


@checkword
def memoryCap():
    """
    UInt64 MemoryCap (read)
    内存容量
    :return: True or False
    """
    result = get_properties_value('MemoryCap')
    if isinstance(result, dbus.UInt64):
        logging.info(f"MemoryCap: {result}")
        return True
    else:
        return False
