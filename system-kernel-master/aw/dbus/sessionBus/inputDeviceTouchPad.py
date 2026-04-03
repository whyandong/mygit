# -*- coding: utf-8 -*-
import dbus
import logging

from frame.decorator import checkword
from aw.dbus.dbus_common import get_session_dbus_interface

DBUS_NAME = 'com.deepin.daemon.InputDevices'
DBUS_PATH = '/com/deepin/daemon/InputDevice/TouchPad'
IFACE_NAME = 'com.deepin.daemon.InputDevice.TouchPad'


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
def disableIfTyping():
    """
    bool DisableIfTyping (readwrite)
    是否在输入时禁用
    :return: True or False
    """
    result = get_properties_value('DisableIfTyping')
    if isinstance(result, dbus.Boolean):
        logging.info(f"是否在输入时禁用: {bool(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


@checkword
def motionAcceleration():
    """
    float64 MotionAcceleration (readwrite)
    移动加速
    :return: True or False
    """
    result = get_properties_value('MotionAcceleration')
    if isinstance(result, dbus.Double):
        logging.info(f"移动加速为: {float(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
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
        logging.info(f"移动阈值为: {float(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
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
        logging.info(f"移动速度范围为: {float(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


@checkword
def deltaScroll():
    """
    int32 DeltaScroll (readwrite)
    滚动变化量
    :return: True or False
    """
    result = get_properties_value('DeltaScroll')
    if isinstance(result, dbus.Int32):
        logging.info(f"滚动变化量为: {int(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
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
        logging.info(f"是否使用自然滚动: {bool(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


@checkword
def horizScroll():
    """
    bool HorizScroll (readwrite)
    是否使用水平滚动
    :return: True or False
    """
    result = get_properties_value('HorizScroll')
    if isinstance(result, dbus.Boolean):
        logging.info(f"是否使用水平滚动: {bool(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


@checkword
def vertScroll():
    """
    bool VertScroll (readwrite)
    是否使用竖直滚动
    :return: True or False
    """
    result = get_properties_value('VertScroll')
    if isinstance(result, dbus.Boolean):
        logging.info(f"是否使用竖直滚动: {bool(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


@checkword
def dragThreshold():
    """
    int32 DragThreshold (readwrite)
    拖动阈值
    :return: True or False
    """
    result = get_properties_value('DragThreshold')
    if isinstance(result, dbus.Int32):
        logging.info(f"是否使用竖直滚动: {int(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


@checkword
def palmMinWidth():
    """
    int32 PalmMinWidth (readwrite)
    手掌误触最小宽度
    :return: True or False
    """
    result = get_properties_value('PalmMinWidth')
    if isinstance(result, dbus.Int32):
        logging.info(f"是否使用竖直滚动: {int(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
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
        logging.info(f"是否存在: {bool(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


@checkword
def tPadEnable():
    """
    bool TPadEnable (readwrite)
    是否开启
    :return: True or False
    """
    result = get_properties_value('TPadEnable')
    if isinstance(result, dbus.Boolean):
        logging.info(f"是否开启: {bool(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


@checkword
def tapClick():
    """
    bool TapClick (readwrite)
    是否点击
    :return: True or False
    """
    result = get_properties_value('TapClick')
    if isinstance(result, dbus.Boolean):
        logging.info(f"是否点击: {bool(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


@checkword
def palmDetect():
    """
    bool PalmDetect (readwrite)
    是否开启手掌误触检测
    :return: True or False
    """
    result = get_properties_value('PalmDetect')
    if isinstance(result, dbus.Boolean):
        logging.info(f"是否开启手掌误触检测: {bool(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


@checkword
def doubleClick():
    """
    int32 DoubleClick (readwrite)
    双击速度
    :return: True or False
    """
    result = get_properties_value('DoubleClick')
    if isinstance(result, dbus.Int32):
        logging.info(f"双击速度: {int(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


@checkword
def palmMinZ():
    """
    int32 PalmMinZ (readwrite)
    手掌误触最低Z轴压力
    :return: True or False
    """
    result = get_properties_value('PalmMinZ')
    if isinstance(result, dbus.Int32):
        logging.info(f"手掌误触最低Z轴压力: {int(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
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
        logging.info(f"设备列表: {str(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
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
        logging.info(f"是否使用左手模式: {bool(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


@checkword
def edgeScroll():
    """
    bool EdgeScroll (readwrite)
    是否使用边缘滚动
    :return: True or False
    """
    result = get_properties_value('EdgeScroll')
    if isinstance(result, dbus.Boolean):
        logging.info(f"是否使用边缘滚动: {bool(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False
