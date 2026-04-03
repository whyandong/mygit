# -*- coding: utf-8 -*-
import time
import logging

import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.api.XEventMonitor'
IFACE_NAME = 'com.deepin.api.XEventMonitor'
DBUS_PATH = '/com/deepin/api/XEventMonitor'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result



def get_registerFullScreen():
    """
    注册屏幕区域
    param:无
    return:String id号
    """
    interface = dbus_interface()
    result = interface.RegisterFullScreen()
    logging.info(f"注册屏幕区域的id值为{result}")
    if isinstance(result, dbus.String):
        logging.info(f"生成的id值为{result}径成功")
        return result
    else:
        logging.info(f"生成id值失败")
        return False


'''======================方法封装＝＝＝＝＝＝＝＝＝＝＝＝'''


@checkword
def beginTouch():
    """
    开始触摸
    param:无
    """
    interface = dbus_interface()
    interface.BeginTouch()
    logging.info("检查接口执行成功")
    return True


@checkword
def debugGetPidAreasMap():
    """
    debug 模式获取触摸区域信息
    param:无
    return:string,触摸区域信息
    """
    interface = dbus_interface()
    result = interface.DebugGetPidAreasMap()
    if isinstance(result, dbus.String):
        logging.info(f"获取音频信息的值成功,map值为{result}")
        return True
    else:
        logging.info(f"获取音频信息的值失败,map值为{result}")
        return False

@checkword
def registerFullScreen():
    """
    注册屏幕区域
    param:无
    return:String id号
    """
    interface = dbus_interface()
    result = interface.RegisterFullScreen()
    logging.info(f"注册屏幕区域的id值为{result}")
    if isinstance(result, dbus.String):
        logging.info(f"生成的id值为{result}径成功")
        return True
    else:
        logging.info(f"生成id值失败")
        return False


@checkword
def registerFullScreenMotionFlag():
    """
    注册屏幕标签
    param:无
    """
    interface = dbus_interface()
    interface.RegisterFullScreenMotionFlag()
    logging.info("检查接口执行成功")
    return True

@checkword
def unRegisterArea(id):
    """
    取消注册屏幕区域
    param:string id
    return:boolean
    """
    interface = dbus_interface()
    result = interface.UnregisterArea(dbus.String(id))
    logging.info(f"取消注册屏幕区域的id值为{id}")
    if isinstance(result, dbus.Boolean):
        logging.info(f"注销的id返回值为{result}")
        return True
    else:
        logging.info(f"注销屏幕区域di值失败")
        return False

@checkword
def unregisterFullScreenMotionFlag():
    """
    注册屏幕标签
    param:无
    """
    interface = dbus_interface()
    interface.UnregisterFullScreenMotionFlag()
    logging.info("检查接口执行成功")
    return True
