# -*- coding: utf-8 -*-
import os
import time
import logging

import dbus

from frame.decorator import checkword
from aw.dbus.systemBus import systemCommon

dbus_name = 'com.deepin.daemon.PowerManager'
dbus_path = '/com/deepin/daemon/PowerManager'
iface_name = 'com.deepin.daemon.PowerManager'


@checkword
def canHibernate():
    """
    判断是否支持休眠
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.CanHibernate()
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info('获取是否支持休眠功能成功')
        return True
    else:
        logging.info('获取是否支持休眠功能失败')
        return False

@checkword
def canReboot():
    """
    判断是否支持重启动
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.CanReboot()
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info('获取是否支持重启功能成功')
        return True
    else:
        logging.info('获取是否支持重启功能失败')
        return False

@checkword
def canShutdown():
    """
    判断是否支持关机
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.CanShutdown()
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info('获取是否支持关机功能成功')
        return True
    else:
        logging.info('获取是否支持关机功能失败')
        return False

@checkword
def canSuspend():
    """
    判断是否支持重启动
    :return:True or False
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.CanSuspend()
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        logging.info('获取是否支持挂起功能成功')

        return True
    else:
        logging.info('获取是否支持挂起功能失败')
        return False

if __name__ == '__main__':
    import sys

    test = canHibernate()
    print(test)