# -*- coding: utf-8 -*-
import re
import time
import logging

import dbus

from frame.decorator import checkword
from aw.dbus.sessionBus import sessionCommon
from aw.dbus.dbus_common import get_session_dbus_interface

dbus_name = 'com.deepin.daemon.Network'
dbus_path = '/com/deepin/daemon/Network'
iface_name = 'com.deepin.daemon.Network'


def dbus_interface():
    return get_session_dbus_interface(dbus_name, dbus_path, iface_name)


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(dbus_name, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(iface_name, properties)
    return result


def getNetworkIface():
    """
    获取网络设备接口
    :return:True or False
    """
    out = sessionCommon.excute_cmd('nmcli conn show')
    logging.info(out)
    net_id = re.findall(r'ethernet\s*(\S*)\s*', out)
    logging.info(net_id[0])
    return net_id[0]


def enableDevice(devPath, type):
    """
    通过路径打开或断开网络
    :param path:如'/org/freedesktop/NetworkManager/Devices/2'
    :param type: disable or enable
    :return:True or False
    """
    time.sleep(1)
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    if type == 'enable':
        dbus_out = property_obj.EnableDevice(devPath, True)
    elif type == 'disable':
        dbus_out = property_obj.EnableDevice(devPath, False)
    else:
        logging.info("传入参数有误，请检查！")
    logging.info(dbus_out)
    time.sleep(1)


"""
=========================功能函数=================================
=========================接口方法=================================
"""


@checkword
def requestWirelessScan():
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    dbus_out = property_obj.RequestWirelessScan()
    logging.info(dbus_out)
    return True

@checkword
def setProxyMethod(method):
    property_obj = sessionCommon.session_bus(dbus_name, dbus_path, iface_name)
    dbus_out = property_obj.SetProxyMethod(method)
    logging.info(dbus_out)
    return True


"""
=========================接口方法=================================
=========================接口属性=================================
"""


@checkword
def networkingEnabled():
    """
    Boolean NetworkingEnabled (read/write),指示当前是否启用了整体联网
    :return:
    """
    result = get_properties_value('NetworkingEnabled')
    if isinstance(result, dbus.Boolean):
        logging.info(f"当前是否启用了整体联网: {type(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


@checkword
def vpnEnabled():
    """
    Boolean VpnEnabled (read/write),指示VPN功能开关是否开启
    :return:
    """
    result = get_properties_value('VpnEnabled')
    if isinstance(result, dbus.Boolean):
        logging.info(f"VPN功能开关是否开启: {type(result)}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


@checkword
def activeConnections():
    """
    String ActiveConnections(read),保存着所有活跃的连接
    :return:
    """
    result = get_properties_value('ActiveConnections')
    if isinstance(result, dbus.String):
        logging.info(f"保存着所有活跃的连接: {result}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


@checkword
def connections():
    """
    String Connections(read),保存这连接的信息
    :return:
    """
    result = get_properties_value('Connections')
    if isinstance(result, dbus.String):
        logging.info(f"保存这连接的信息: {result}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


@checkword
def devices():
    """
    String Devices (read),所有网卡设备信息,比如无线网卡
    :return:
    """
    result = get_properties_value('Devices')
    if isinstance(result, dbus.String):
        logging.info(f"所有网卡设备信息: {result}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


@checkword
def wirelessAccessPoints():
    """
    String WirelessAccessPoints (read),无线wifi列表, RequestWirelessScan()接口被调用时会被刷新一次, 并且每分钟会被刷新一次
    :return:
    """
    result = get_properties_value('WirelessAccessPoints')
    if isinstance(result, dbus.String):
        logging.info(f"无线wifi列表: {result}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


@checkword
def connectivity():
    """
    Uint32 Connectivity (read),网络连接状态
    :return:
    """
    result = get_properties_value('Connectivity')
    if isinstance(result, dbus.UInt32):
        logging.info(f"网络连接状态: {result}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


@checkword
def state():
    """
    Uint32 State (read),NetworkManager守护程序的整体状态
    :return:
    """
    result = get_properties_value('State')
    if isinstance(result, dbus.UInt32):
        logging.info(f"网络连接状态: {result}")
        return True
    else:
        logging.info(f'返回数据类型不正确，实际类型为{type(result)}')
        return False


if __name__ == '__main__':
    requestWirelessScan()
