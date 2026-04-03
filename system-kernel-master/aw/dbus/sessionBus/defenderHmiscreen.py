# -*- coding: utf-8 -*-
import logging

import dbus
import time

from aw.dbus.dbus_common import get_session_dbus_interface
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.defender.hmiscreen'
DBUS_PATH = '/com/deepin/defender/hmiscreen'
IFACE_NAME = 'com.deepin.defender.hmiscreen'


def dbus_interface():
    return get_session_dbus_interface(DBUS_NAME, DBUS_PATH, IFACE_NAME)


def get_properties_value(properties: str):
    property_obj = get_session_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


def set_properties_value(properties: str, value):
    property_obj = get_session_dbus_interface(DBUS_NAME, DBUS_PATH, iface_name='org.freedesktop.DBus.Properties')
    property_obj.Set(IFACE_NAME, properties, value)


@checkword
def show():
    """
    弹出安全中心主界面
    :param: 无
    :return:True or False
    """
    interface = dbus_interface()
    interface.Show()
    return True


@checkword
def showModule(module):
    """
    弹出安全中心模块界面
    :param: module String
    :return:True or False
    """
    interface = dbus_interface()
    interface.ShowModule(module)
    return True


@checkword
def showPage(module,page):
    """
    切换到安全中心某个功能模块
    :param:module String
    :param: page String
    :return:True or False
    """
    interface = dbus_interface()
    interface.ShowPage(module,page)
    return True


@checkword
def exitApp():
    """
    退出defender
    :param:无
    :return:True or False
    """
    interface = dbus_interface()
    interface.ExitApp()
    time.sleep(3)
    return True



@checkword
def showSettingDialog(groupkey):
    """
    显示设置弹框
    :param: groupKey String
    :return:True or False
    """
    interface = dbus_interface()
    interface.showSettingDialog(groupkey)
    return True


@checkword
def showScanByPath(path):
    """
    右键病毒查杀调用此接口
    :param: path String
    :return:True or False
    """
    interface = dbus_interface()
    interface.showScanByPath(path)
    return True



@checkword
def showFuncConnectNetControl(dkgname):
    """
    显示联网管控界面，表格定位到相应数据
    :param: dkgname String
    :return:True or False
    """
    interface = dbus_interface()
    interface.showFuncConnectNetControl(dkgname)
    return True


@checkword
def showFuncConnectRemControl(dkgname):
    """
    显示远程访问状态设置弹框
    :param: dkgname String
    :return:True or False
    """
    interface = dbus_interface()
    interface.showFuncConnectRemControl(dkgname)
    return True


@checkword
def showFuncConnectDataUsage():
    """
    显示流量详情界面
    :param: dkgname String
    :return:True or False
    """
    interface = dbus_interface()
    interface.showFuncConnectDataUsage()
    time.sleep(3)
    return True

