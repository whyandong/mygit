# -*- coding:utf-8 -*-
import dbus
import logging

from frame.decorator import checkword
from aw.dbus.dbus_common import get_session_dbus_interface

DBUS_NAME = 'com.deepin.daemon.InputDevices'
DBUS_PATH = '/com/deepin/daemon/InputDevice/Mouse'
IFACE_NAME = 'com.deepin.daemon.InputDevice.Mouse'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


@checkword
def reset():
    """
    Reset() -> ()
    重置
    :return: True
    """
    interface = dbus_interface()
    interface.Reset()
    return True


@checkword
def dragThreshold():
    """
    int32 DragThreshold (readwrite)
    拖动阈值
    :return: True or False
    """
    result = get_properties_value('DragThreshold')
    if isinstance(result, dbus.Int32):
        logging.info(f"拖动阈值: {result}")
        return True
    else:
        return False


@checkword
def exist():
    """
    bool Exist (read)
    是否存在
    :return: True or False
    """
    result = get_properties_value('Exist')
    if isinstance(result, dbus.Boolean):
        logging.info(f"是否存在: {result}")
        return True
    else:
        return False


@checkword
def disableTpad():
    """
    bool DisableTpad (readwrite)
    是否禁用触摸板
    :return: True or False
    """
    result = get_properties_value('DisableTpad')
    if isinstance(result, dbus.Boolean):
        logging.info(f"是否禁用触摸板: {result}")
        return True
    else:
        return False


@checkword
def adaptiveAccelProfile():
    """
    bool AdaptiveAccelProfile (readwrite)
    是否使用自适应加速配置
    :return: True or False
    """
    result = get_properties_value('AdaptiveAccelProfile')
    if isinstance(result, dbus.Boolean):
        logging.info(f"是否使用自适应加速配置: {result}")
        return True
    else:
        return False


@checkword
def motionAcceleration():
    """
    float64 MotionAcceleration (readwrite)
    移动速度
    :return: True or False
    """
    result = get_properties_value('MotionAcceleration')
    if isinstance(result, dbus.Double):
        logging.info(f"移动速度: {result}")
        return True
    else:
        return False


@checkword
def motionThreshold():
    """
    float64 MotionThreshold (readwrite)
    移动阈值
    :return: True or False
    """
    result = get_properties_value('MotionThreshold')
    if isinstance(result, dbus.Double):
        logging.info(f"移动阈值: {result}")
        return True
    else:
        return False


@checkword
def motionScaling():
    """
    float64 MotionScaling (readwrite)
    移动速度范围
    :return: True or False
    """
    result = get_properties_value('MotionScaling')
    if isinstance(result, dbus.Double):
        logging.info(f"移动速度范围: {result}")
        return True
    else:
        return False


@checkword
def deviceList():
    """
    string DeviceList (read)
    设备列表
    :return: True or False
    """
    result = get_properties_value('DeviceList')
    if isinstance(result, dbus.String):
        logging.info(f"设备列表: {result}")
        return True
    else:
        return False


@checkword
def leftHanded():
    """
    bool LeftHanded (readwrite)
    是否使用左手模式
    :return: True or False
    """
    result = get_properties_value('LeftHanded')
    if isinstance(result, dbus.Boolean):
        logging.info(f"是否使用左手模式: {result}")
        return True
    else:
        return False


@checkword
def naturalScroll():
    """
    bool NaturalScroll (readwrite)
    是否使用自然滚动
    :return: True or False
    """
    result = get_properties_value('NaturalScroll')
    if isinstance(result, dbus.Boolean):
        logging.info(f"是否使用自然滚动: {result}")
        return True
    else:
        return False


@checkword
def middleButtonEmulation():
    """
    bool MiddleButtonEmulation (readwrite)
    是否模拟中键
    :return: True or False
    """
    result = get_properties_value('MiddleButtonEmulation')
    if isinstance(result, dbus.Boolean):
        logging.info(f"是否模拟中键: {result}")
        return True
    else:
        return False


@checkword
def doubleClick():
    """
    int32 DoubleClick (readwrite)
    双击间隔
    :return: True or False
    """
    result = get_properties_value('DoubleClick')
    if isinstance(result, dbus.Int32):
        logging.info(f"双击间隔: {result}")
        return True
    else:
        return False
