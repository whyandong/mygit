# -*- coding: utf-8 -*-
import time
import dbus
import logging

from aw.dbus.systemBus import systemCommon
from frame.decorator import checkword

dbus_name = 'com.deepin.daemon.Gesture'
dbus_path = '/com/deepin/daemon/Gesture'
iface_name = 'com.deepin.daemon.Gesture'


@checkword
def setShortPressDuration(duration):
    """
    设置触控屏短按超时时间(system)
    :param duration:超时时间
    :return:True
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    logging.info(f'system设置触控屏短按超时时间为{duration}')
    property_obj.SetShortPressDuration(duration)
    return True


@checkword
def setEdgeMoveStopDuration(duration):
    """
    设置边缘划入停止手势停止超时时间(system)
    :param duration:超时时间
    :return:True
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    logging.info(f'system设置边缘划入停止手势停止超时时间为{duration}')
    property_obj.SetEdgeMoveStopDuration(duration)
    return True


@checkword
def setDblclickDuration(duration):
    """
    设置双击超时时间(system)
    :param duration:超时时间
    :return:True
    """
    property_obj = systemCommon.system_bus(dbus_name, dbus_path, iface_name)
    logging.info(f'system设置双击超时时间为{duration}')
    property_obj.SetDblclickDuration(duration)
    return True
