# -*- coding: utf-8 -*-
import time
import dbus
import logging

from frame.decorator import checkword
from aw.dbus.dbus_common import get_system_dbus_interface

DBUS_NAME = 'com.deepin.daemon.AirplaneMode'
DBUS_PATH = '/com/deepin/daemon/AirplaneMode'
IFACE_NAME = 'com.deepin.daemon.AirplaneMode'


# ===========================
#         功能函数
# ===========================
def system_bus(dbus_name=DBUS_NAME, dbus_path=DBUS_PATH,
               iface_name=DBUS_NAME):
    system_bus = dbus.SystemBus()
    system_obj = system_bus.get_object(dbus_name, dbus_path)
    property_obj = dbus.Interface(system_obj, dbus_interface=iface_name)
    return property_obj


def dbus_interface():
    return get_system_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_system_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


@checkword
def enable(mode):
    """
    设置飞行模式开关，True:开启; False:关闭
    :return: 无
    """
    interface = system_bus()
    if mode:
        interface.Enable(dbus.Boolean(mode))
        logging.info(f"飞行模式开关开启({mode})设置中...")
        return True
    elif not mode:
        interface.Enable(dbus.Boolean(mode))
        logging.info(f"飞行模式开关关闭({mode})设置中...")
        return True
    else:
        logging.info(f"飞行模式开关状态值({mode})传入有误！")
        return False


@checkword
def enableBluetooth(mode):
    """
    设置蓝牙设备开关，True:开启; False:关闭
    :return: 无
    """
    interface = system_bus()
    if mode:
        interface.EnableBluetooth(dbus.Boolean(mode))
        logging.info(f"蓝牙设备开关开启({mode})设置中...")
        return True
    elif not mode:
        interface.EnableBluetooth(dbus.Boolean(mode))
        logging.info(f"蓝牙设备开关关闭({mode})设置中...")
        return True
    else:
        logging.info(f"蓝牙设备开关值({mode})传入有误！")
        return False


@checkword
def enableWifi(mode):
    """
    设置WIFI开关，True:开启; False:关闭
    :return: 无
    """
    interface = system_bus()
    if mode:
        interface.EnableWifi(dbus.Boolean(mode))
        logging.info(f"WIFI开关开启({mode})设置中...")
        return True
    elif not mode:
        interface.EnableWifi(dbus.Boolean(mode))
        logging.info(f"WIFI开关关闭({mode})设置中...")
        return True
    else:
        logging.info(f"WIFI开关值({mode})传入有误！")
        return False


@checkword
def dumpState():
    """
    调用DumpState(),直接开启代码调试
    :return: 无
    """
    interface = system_bus()
    result = interface.DumpState()
    logging.info(result)
    return True


@checkword
def checkenable(mode):
    """
     飞行模式开状态检验，True:开启; False:关闭，检验设置后开关状态是否一致
    :return: 无
    """
    time.sleep(2)
    result = get_properties_value('Enabled')
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        if mode == 'True':
            if result:
                logging.info(f"返回飞行模式开关状态类型Boolean正常，且设置状态({mode})生效")
                return True
            else:
                logging.info(f"返回飞行模式开关状态类型Boolean正常，设置状态({mode})未生效，返回状态：{result}")
                return False
        elif mode == 'False':
            if not result:
                logging.info(f"返回飞行模式开关状态类型Boolean正常，且设置状态({mode})生效")
                return True
            else:
                logging.info(f"返回飞行模式开关状态类型Boolean正常，设置({mode})未生效，返回状态：{result}")
                return False
    else:
        logging.info(f"返回飞行模式开关状态类型Boolean异常，返回值类型{type(result)}")
        return False


@checkword
def checkenableBluetooth(mode):
    """
     蓝牙设备开关状态检验，True:开启; False:关闭，检验设置后开关状态是否一致
    :return: 无
    """
    time.sleep(1)
    result = get_properties_value('BluetoothEnabled')
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        if mode == 'True':
            if result:
                logging.info(f"返回蓝牙设备开关状态类型Boolean正常，且设置状态({mode})生效")
                return True
            else:
                logging.info(f"返回蓝牙设备开关状态类型Boolean正常，设置状态({mode})未生效，返回状态：{result}")
                return False
        elif mode == 'False':
            if not result:
                logging.info(f"返回蓝牙设备开关状态类型Boolean正常，且设置状态({mode})生效")
                return True
            else:
                logging.info(f"返回蓝牙设备开关状态类型Boolean正常，设置({mode})未生效，返回状态：{result}")
                return False
    else:
        logging.info(f"返回蓝牙设备开关状态类型Boolean异常，返回值类型{type(result)}")
        return False


@checkword
def checkenableWifi(mode):
    """
    Wifi开关状态检验，True:开启; False:关闭，检验设置后开关状态是否一致
    :return: 无
    """
    time.sleep(1)
    result = get_properties_value('WifiEnabled')
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        if mode == 'True':
            if result:
                logging.info(f"返回Wifi开关状态类型Boolean正常，且设置状态({mode})生效")
                return True
            else:
                logging.info(f"返回Wifi开关状态类型Boolean正常，设置状态({mode})未生效，返回状态：{result}")
                return False
        elif mode == 'False':
            if not result:
                logging.info(f"返回Wifi开关状态类型Boolean正常，且设置状态({mode})生效")
                return True
            else:
                logging.info(f"返回Wifi开关状态类型Boolean正常，设置({mode})未生效，返回状态：{result}")
                return False
    else:
        logging.info(f"返回Wifi开关状态类型Boolean异常，返回值类型{type(result)}")
        return False
