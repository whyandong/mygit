# -*- coding: utf-8 -*-
import time
import logging

import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.daemon.Network'
IFACE_NAME = 'com.deepin.daemon.Network'
DBUS_PATH = '/com/deepin/daemon/Network'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result




'''======================方法封装＝＝＝＝＝＝＝＝＝＝＝＝'''


@checkword
def getActiveConnectionInfo():
    """
    获取有线,无线,VPN三者的活跃网络连接信息,以JSON字符串的形式返回
    param:无
    return:aclinfosjson:有线,无线,三种网络的信息
    """
    interface = dbus_interface()
    result = interface.GetActiveConnectionInfo()
    if isinstance(result, dbus.String):
        logging.info(f"获取活动网络信息的值成功,网络信息值为{result}")
        return True
    else:
        logging.info(f"获取活动网络信息的值失败,值为{result}")
        return False



@checkword
def getAutoProxy():
    """
    获取代理一个PAC文件的URL的值,通过gsettings获取
    param:无
    return:proxyAuto,一个URL值
    """
    interface = dbus_interface()
    result = interface.GetAutoProxy()
    if isinstance(result, dbus.String):
        logging.info(f"获取自动代理文件代理值成功,代理文件值为{result}")
        return True
    else:
        logging.info(f"获取自动代理值失败,获取到的值为{result}")
        return False

@checkword
def getProxyIgnoreHosts():
    """
    获取因为被","分割的代理网络字符串而被忽略服务器,也是通过gsettings获取一个字符串
    param:无
    return:String ignoreHosts被忽略的服务器名
    """
    interface = dbus_interface()
    result = interface.GetProxyIgnoreHosts()
    logging.info(f"被忽略的服务器名值为{result}")
    if isinstance(result, dbus.String):
        return True
    else:
        logging.info(f"获取被忽略的服务器名失败,失败值为{result}")
        return False


@checkword
def getProxyMethod():
    """
    通过gsettings获取当前代理的方法, 会返回"none", "manual","auto"
    param:无
    return:proxyMode: string,代理模式
    """
    interface = dbus_interface()
    result = interface.GetProxyMethod()

    if isinstance(result, dbus.String):
        logging.info(f"获取当前代理模式{result}")
        return True
    else:
        logging.info(f"获取当前代理模式失败,失败信息返回值为{result}")
        return False

@checkword
def getSupportedConnectionTypes():
    """
    此方法返回所有支持的连接类型
    param:无
    return:string,所有支持的连接类型
    """
    interface = dbus_interface()
    result = interface.GetSupportedConnectionTypes()

    if isinstance(result, dbus.Array):
        logging.info(f"获取所支持的连接类型值成功,为{result}")
        return True
    else:
        logging.info(f"获取所支持的连接类型值失败,返回类型为{type(result)}")
        return False

@checkword
def requestWirelessScan():
    """
    请求扫描, 会对每个设备扫描一次,更新属性WirelessAccessPoints属性,并返回一个apList给前端用于更新wifi列表
    param:无
    """
    interface = dbus_interface()
    interface.RequestWirelessScan()
    logging.info("检查接口执行成功")
    return True


"""=================================属性方法==========================================="""


@checkword
def getNetworkingEnabled():
    """
    指示当前是否启用了整体联网。
    :return:Boolean
    """
    result = get_properties_value('NetworkingEnabled')
    if isinstance(result, dbus.Boolean):
        logging.info("获取是否开启了整体联网成功")
        return True
    else:
        logging.info(f"获取是否开启了整体联网失败,获取到的值的类型为{type(result)}")
        return False


@checkword
def getVpnEnabled():
    """
    指示VPN功能开关是否开启。
    :return:Boolean
    """
    result = get_properties_value('VpanEnabled')
    if isinstance(result, dbus.Boolean):
        logging.info("获取VPN开关属性成功")
        return True
    else:
        logging.info(f"获取VPN开关属性失败,获取到的值的类型为{type(result)}")
        return False


@checkword
def getActiveConnections():
    """
    保存所有活动连接。
    :return:String
    """
    result = get_properties_value('ActiveConnections')
    if isinstance(result, dbus.String):
        logging.info("获取保存所有活动连接属性成功")
        return True
    else:
        logging.info(f"获取保存所有活动连接属性失败,获取到的值的类型为{type(result)}")
        return False

@checkword
def getConnections():
    """
    保存连接的信息。
    :return:String
    """
    result = get_properties_value('Connections')
    if isinstance(result, dbus.String):
        logging.info("获取保存连接属性成功")
        return True
    else:
        logging.info(f"获取保存连接信息属性失败,获取到的值的类型为{type(result)}")
        return False


@checkword
def getDevices():
    """
    所有网卡设备信息,比如无线网卡。
    :return:String
    """
    result = get_properties_value('Devices')
    if isinstance(result, dbus.String):
        logging.info("获取保所有网卡的信息成功")
        return True
    else:
        logging.info(f"获取所有网卡信息属性失败,获取到的值的类型为{type(result)}")
        return False


@checkword
def getWirelessAccessPoints():
    """
    无线wifi列表, RequestWirelessScan()接口被调用时会被刷新一次, 并且每分钟会被刷新一次。
    :return:String
    """
    result = get_properties_value('WirelessAccessPoints')
    if isinstance(result, dbus.String):
        logging.info("获取无线wifi列表刷新信息成功")
        return True
    else:
        logging.info(f"获取无线wifi列表刷新失败,获取到的值的类型为{type(result)}")
        return False

@checkword
def getConnectivity():
    """
    网络连接状态。
    :return:String
    """
    result = get_properties_value('Connectivity')
    if isinstance(result, dbus.UInt32):
        logging.info("获取网络连接状态成功")
        return True
    else:
        logging.info(f"获取网络连接状态失败,获取到的值的类型为{type(result)}")
        return False

@checkword
def getState():
    """
    NetworkManager守护程序的整体状态。
    :return:String
    """
    result = get_properties_value('State')
    if isinstance(result, dbus.UInt32):
        logging.info("获取NetworkManager守护程序的整体状态成功")
        return True
    else:
        logging.info(f"获取NetworkManager守护程序的整体状态失败,获取到的值的类型为{type(result)}")
        return False