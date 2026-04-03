# -*- coding: utf-8 -*-
# com.deepin.dde.controlcenter相关
import os
import time
import logging

import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.dde.ControlCenter'
DBUS_PATH = '/com/deepin/dde/ControlCenter'
IFACE_NAME = 'com.deepin.dde.ControlCenter'


# ===========================
#         功能函数
# ===========================
def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


@checkword
def exitProc():
    """
    退出控制中心
    :param 无
    :return:True
    """
    time.sleep(1)
    interface = dbus_interface()
    interface.exitProc()
    return True


@checkword
def hide():
    """
    隐藏控制中心
    :param 无
    :return:True
    """
    time.sleep(1)
    interface = dbus_interface()
    interface.Hide()
    return True





@checkword
def show():
    """
    显示控制中心
    :param 无
    :return:True
    """
    time.sleep(1)
    interface = dbus_interface()
    interface.Show()
    return True

@checkword
def showImmediately():
    """
    显示控制中心，控制中心最小化时有效
    :param 无
    :return:无
    """
    time.sleep(1)
    interface = dbus_interface()
    interface.ShowImmediately()
    return True

@checkword
def showHome():
    """
    打开控制中心首页
    :param 无
    :return:True
    """
    time.sleep(1)
    interface = dbus_interface()
    interface.ShowHome()
    return True

@checkword
def showModule(module):
    """
    显示控制中心模块
    :param module string 模块名称
    :return:True
    """
    time.sleep(1)
    interface = dbus_interface()
    interface.ShowModule(dbus.String(module))
    return True

@checkword
def showPage(module,page):
    """
    显示控制中心模块下的页面
    :param module string 模块名称
    :param page string 页面名称
    :return:True
    """
    time.sleep(1)
    interface = dbus_interface()
    interface.ShowPage(dbus.String(module),dbus.String(page))
    return True

@checkword
def toggle():
    """
    切换控制中心显示状态
    :param 无
    :return:True
    """
    time.sleep(1)
    interface = dbus_interface()
    interface.Toggle()
    return True


@checkword
def toggleInLeft():
    """
    切换控制中心显示状态
    :param 无
    :return:True
    """
    interface = dbus_interface()
    interface.ToggleInLeft()
    return True

@checkword
def isModuleAvailable(module):
    """
    模块是否可用
    :param module String 模块名
    :return:Boolean
    """
    time.sleep(2)
    interface = dbus_interface()
    result = interface.isModuleAvailable(dbus.String(module))
    if isinstance(result,dbus.Boolean):
        return True
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False


@checkword
def isNetworkCanShowPassword():
    """
    网络是否需要密码
    :param 无
    :return:Boolean
    """
    interface = dbus_interface()
    result = interface.isNetworkCanShowPassword()
    if isinstance(result,dbus.Boolean):
        return True
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False
'================属性方法==================='


def showInRight():
    """
    是否在右边
    """
    time.sleep(2)
    result = get_properties_value(dbus.String('ShowInRight'))
    logging.info(result)
    if isinstance(result, dbus.Boolean):
        return True
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False

def rect():
    """
    方向
    """
    result = get_properties_value(dbus.String('Rect'))
    logging.info(result)
    if isinstance(result, dbus.Struct):
        return True
    else:
        logging.info(f'返回类型错误，返回数据类型为{type(result)}')
        return False


if __name__ == '__main__':
    visible()
