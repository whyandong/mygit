# -*- coding: utf-8 -*-
import os
import time
import logging

import dbus

from frame.decorator import checkword
from aw.dbus.systemBus import systemCommon

dbus_name = 'com.deepin.system.Bluetooth'
dbus_path = '/com/deepin/system/Bluetooth'
iface_name = 'com.deepin.system.Bluetooth'


@checkword
def clearUnpairedDevice():
    """
    删除所有未配对设备
    :return:None
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.ClearUnpairedDevice()
    logging.info(result)
    return True

@checkword
def debugInfo():
    """
    获取调试信息
    :return:String
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.DebugInfo()
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info('获取调试信息成功')
        return True
    else:
        logging.info('获取调试信息失败')
        return False

@checkword
def getAdapters():
    """
    获取所有适配器
    :return:String
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.GetAdapters()
    logging.info(result)
    if isinstance(result, dbus.String):
        logging.info('获取所有适配器成功')
        return True
    else:
        logging.info('获取所有适配器失败')
        return False

#=================属性方法==========================================================
@checkword
def getCanSendFile():
    """
    在内核可能禁止文件发送时，判断能否发送文件
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.CanSendFile()
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info('获取判断能否发送文件成功')

        return True
    else:
        logging.info('获取判断能否发送文件失败')
        return False

@checkword
def getState():
    """
    表示蓝牙的状态（不可用，可用，已连接）
    :return:Uint32
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.State()
    logging.info(result)
    if isinstance(result, dbus.UInt32):
        logging.info('获取蓝牙的状态成功')

        return True
    else:
        logging.info('获取蓝牙的状态失败')
        return False

if __name__ == '__main__':
    import sys

    debugInfo()
    print()