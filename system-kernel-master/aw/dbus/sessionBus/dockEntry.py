# -*- coding: utf-8 -*-
import time
import logging

import dbus

from aw.dbus.dbus_common import get_session_dbus_interface
from frame.decorator import checkword

DBUS_NAME = 'com.deepin.dde.daemon.Dock'
IFACE_NAME = 'com.deepin.dde.daemon.Dock.Entry'

def dbus_interface(dbus_path):
    return get_session_dbus_interface(DBUS_NAME, dbus_path, IFACE_NAME)

def get_properties_value(properties: str, dbus_path):
    property_obj = get_session_dbus_interface(DBUS_NAME, dbus_path, iface_name='org.freedesktop.DBus.Properties')
    result = property_obj.Get(IFACE_NAME, properties)
    return result


def get_entries_path_list():
    result = get_properties_value('Entries', '/com/deepin/dde/daemon/Dock')
    dbus_path_list = [str(path) for path in result]
    return dbus_path_list


def get_entry_path_by_name(entry_name="文件管理器"):
    dbus_path_list = get_entries_path_list()
    for item in dbus_path_list:
        interface = get_session_dbus_interface(DBUS_NAME, item, iface_name='org.freedesktop.DBus.Properties')
        if entry_name == str(interface.Get(IFACE_NAME, 'Name')):
            return item
    else:
        raise ValueError(f'未找到属性Name为{entry_name}的Entry对象')


'''======================方法封装＝＝＝＝＝＝＝＝＝＝＝＝'''


@checkword
def check(dbus_path):
    interface = dbus_interface(dbus_path)
    interface.Check()
    logging.info("检查接口执行成功")
    return True


@checkword
def forceQuit(dbus_path):
    interface = dbus_interface(dbus_path)
    interface.ForceQuit()
    logging.info("检查接口执行成功")
    return True


@checkword
def getAllowedCloseWindows(dbus_path):
    interface = dbus_interface(dbus_path)
    result = interface.GetAllowedCloseWindows
    logging.info(f'获取到的windows信息为{result}')
    if isinstance(result, dbus.Array):
        logging.info("windows会话的值成功")
        return True
    else:
        logging.info("获取windows会话的值失败")
        return False

@checkword
def presentWindows(dbus_path):
    interface = dbus_interface(dbus_path)
    interface.PresentWindows()
    logging.info('检查接口执行成功')
    return True

@checkword
def requestDock(dbus_path):
    interface = dbus_interface(dbus_path)
    interface.RequestDock()
    logging.info("检查接口成功")
    return True


@checkword
def requestUnDock(dbus_path):
    interface = dbus_interface(dbus_path)
    interface.RequestUnDock()
    logging.info("检查接口成功")
    return True


'''======================属性方法====================='''

@checkword
def isActive(dbus_path):
    """
    bool IsActive (read):当前entry关联的程序是否处于焦点激活状态
    :param dbus_path:
    :return:True or False
    """
    result = get_properties_value(dbus.String('IsActive'), dbus_path)
    if isinstance(result, dbus.Boolean):
        logging.info(f'当前entry关联的程序是否处于焦点激活状态:{bool(result)}')
        return True

    else:
        logging.info('返回数据类型不匹配')
        logging.info(f'返回数据类型为：{type(result)}')
        return False


@checkword
def isDocked(dbus_path):
    """
    bool IsDocked (read):当前entry关联的程序是否常驻在dock上
    :param dbus_path:
    :return:True or False
    """
    result = get_properties_value(dbus.String('IsDocked'), dbus_path)
    if isinstance(result, dbus.Boolean):
        logging.info(f'当前entry关联的程序是否常驻在dock上:{bool(result)}')
        return True

    else:
        logging.info('返回数据类型不匹配')
        logging.info(f'返回数据类型为：{type(result)}')
        return False


@checkword
def windowInfos(dbus_path):
    """
    map[uint32]struct{string,bool} WindowInfos (read):当前entry关联的程序的窗口实例id信息 key表示每个窗口实例id，
                                                      string字段为窗口的title描述
    :param dbus_path:entry的dbus路径
    :return:True or False
    """
    result = get_properties_value(dbus.String('WindowInfos'), dbus_path)
    logging.info(f'获取到的windows信息为{result}')
    if isinstance(result, dbus.Dictionary):
        logging.info("windows会话的值成功")
        return True
    else:
        logging.info("获取windows会话的值失败")
        return False


@checkword
def desktopFile(dbus_path):
    """
    string DesktopFile (read):当前entry关联的程序的desktopFile路径
    :param dbus_path:
    :return:True or False
    """
    result = get_properties_value(dbus.String('DesktopFile'), dbus_path)
    if isinstance(result, dbus.String):
        logging.info(f'当前entry关联的程序的desktopFile路径:{str(result)}')
        return True

    else:
        logging.info('返回数据类型不匹配')
        logging.info(f'返回数据类型为：{type(result)}')
        return False


@checkword
def icon(dbus_path):
    """
    string Icon (read):当前entry关联的程序的icon路径
    :param dbus_path:
    :return:True or False
    """
    result = get_properties_value(dbus.String('Icon'), dbus_path)
    if isinstance(result, dbus.String):
        logging.info(f'当前entry关联的程序的icon路径:{str(result)}')
        return True

    else:
        logging.info('返回数据类型不匹配')
        logging.info(f'返回数据类型为：{type(result)}')
        return False


@checkword
def id_(dbus_path):  # 和内置函数冲突加下滑线区别
    """
    string Id (read):当前entry关联的程序的id
    :param dbus_path:
    :return:True or False
    """
    result = get_properties_value(dbus.String('Id'), dbus_path)
    if isinstance(result, dbus.String):
        logging.info(f'当前entry关联的程序的id:{str(result)}')
        return True

    else:
        logging.info('返回数据类型不匹配')
        logging.info(f'返回数据类型为：{type(result)}')
        return False


@checkword
def menu(dbus_path):
    """
    string Menu (read):dock栏点右键点击当前entry关联的程序，弹出的菜单选项
    :param dbus_path:
    :return:True or False
    """
    result = get_properties_value(dbus.String('Menu'), dbus_path)
    if isinstance(result, dbus.String):
        logging.info(f'dock栏点右键点击当前entry关联的程序:{str(result)}')
        return True

    else:
        logging.info('返回数据类型不匹配')
        logging.info(f'返回数据类型为：{type(result)}')
        return False

@checkword
def name(dbus_path):
    """
    string Name (read):当前entry关联的程序的name
    :param dbus_path:
    :return:True or False
    """
    result = get_properties_value(dbus.String('Name'), dbus_path)
    if isinstance(result, dbus.String):
        logging.info(f'当前entry关联的程序的name:{str(result)}')
        return True

    else:
        logging.info('返回数据类型不匹配')
        logging.info(f'返回数据类型为：{type(result)}')
        return False


@checkword
def currentWindow(dbus_path):
    """
    uint32 CurrentWindow (read):当前显示在最前端的窗口的id
    :param dbus_path:
    :return:True or False
    """
    result = get_properties_value(dbus.String('CurrentWindow'), dbus_path)
    if isinstance(result, dbus.UInt32):
        logging.info(f'当前显示在最前端的窗口的id:{int(result)}')
        return True

    else:
        logging.info('返回数据类型不匹配')
        logging.info(f'返回数据类型为：{type(result)}')
        return False


