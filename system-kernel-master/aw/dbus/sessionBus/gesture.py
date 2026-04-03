# -*- coding: utf-8 -*-
import time
import dbus
import logging

from aw.dbus.sessionBus import sessionCommon
from frame.decorator import checkword

dbus_name = 'com.deepin.daemon.Gesture'
dbus_path = '/com/deepin/daemon/Gesture'
iface_name = 'com.deepin.daemon.Gesture'


def setShortPressDuration(duration):
    """
    设置触控屏短按超时时间
    :param duration:超时时间
    :return:None
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    logging.info(f'设置触控屏短按超时时间为{duration}')
    property_obj.SetShortPressDuration(duration)


def getShortPressDuration():
    """
    获取触控屏短按超时时间
    :return:dbus.UInt32
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.GetShortPressDuration()
    return result


@checkword
def checkSetShortPressDuration(duration):
    """
    检查设置触控屏短按超时时间状态
    :param duration:超时时间
    :return:True or False
    """
    ret = getShortPressDuration()
    if ret == duration:
        logging.info(f"检查设置触控屏短按超时时间为{duration}成功")
        return True
    else:
        logging.info(f"检查设置触控屏短按超时时间为{duration}失败")
        return False


@checkword
def getShortPressDurationValue():
    """
    获取触控屏短按超时时间值
    :return:True or False
    """
    ret = getShortPressDuration()
    if isinstance(ret, dbus.UInt32):
        logging.info("获取触控屏短按超时时间值成功")
        return True
    else:
        logging.info("获取触控屏短按超时时间值失败")
        return False


def setLongPressDuration(duration):
    """
    设置触控屏长按超时时间
    :param duration:超时时间
    :return:None
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    logging.info(f'设置触控屏长按超时时间为{duration}')
    property_obj.SetLongPressDuration(duration)


def getLongPressDuration():
    """
    获取触控屏长按超时时间
    :return:dbus.UInt32
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.GetLongPressDuration()
    return result


@checkword
def checkSetLongPressDuration(duration):
    """
    检查设置触控屏长按超时时间状态
    :param duration:超时时间
    :return:True or False
    """
    ret = getLongPressDuration()
    if ret == duration:
        logging.info(f"检查设置触控屏长按超时时间为{duration}成功")
        return True
    else:
        logging.info(f"检查设置触控屏长按超时时间为{duration}失败")
        return False


@checkword
def getLongPressDurationValue():
    """
    获取触控屏长按超时时间值
    :return:True or False
    """
    ret = getLongPressDuration()
    if isinstance(ret, dbus.UInt32):
        logging.info("获取触控屏长按超时时间值成功")
        return True
    else:
        logging.info("获取触控屏长按超时时间值失败")
        return False


def setEdgeMoveStopDuration(duration):
    """
    设置触控屏边缘划入后停留时间
    :param duration:超时时间
    :return:None
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    logging.info(f'设置触控屏边缘划入后停留时间为{duration}')
    property_obj.SetEdgeMoveStopDuration(duration)


def getEdgeMoveStopDuration():
    """
    获取触控屏边缘划入后停留时间
    :return:dbus.UInt32
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    result = property_obj.GetEdgeMoveStopDuration()
    return result


@checkword
def checkSetEdgeMoveStopDuration(duration):
    """
    检查设置触控屏边缘划入后停留时间状态
    :param duration:超时时间
    :return:True or False
    """
    ret = getEdgeMoveStopDuration()
    if ret == duration:
        logging.info(f"检查设置触控屏边缘划入后停留时间为{duration}成功")
        return True
    else:
        logging.info(f"检查设置触控屏边缘划入后停留时间为{duration}失败")
        return False


@checkword
def getEdgeMoveStopDurationValue():
    """
    获取触控屏边缘划入后停留时间值
    :return:True or False
    """
    ret = getEdgeMoveStopDuration()
    if isinstance(ret, dbus.UInt32):
        logging.info("获取触控屏边缘划入后停留时间值成功")
        return True
    else:
        logging.info("获取触控屏边缘划入后停留时间值失败")
        return False


@checkword
def getInfos():
    """
    获取手势信息
    :return:True or False
    """
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    ret = property_obj.Get('com.deepin.daemon.Gesture', 'Infos')
    if isinstance(ret, dbus.Array):
        logging.info("获取手势信息成功")
        return True
    else:
        logging.info("获取手势信息失败")
        return False
